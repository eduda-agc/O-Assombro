#version 150 core

// Dados interpolados pelo rasterizador a partir das saidas do vertex shader.
in vec2 out_texture;
in vec3 FragPos;
in vec3 Normal;

// Cor final escrita no framebuffer.
out vec4 FragColor;

// Textura associada ao objeto que esta sendo desenhado.
uniform sampler2D imagem;

#define NUM_LIGHTS 7

// Fontes de luz:
// 0 = lanterna da camera, 1 e 2 = farois, 3 a 6 = velas.
uniform vec3 lightPos[NUM_LIGHTS];
uniform vec3 lightDir[NUM_LIGHTS];
uniform vec3 lightColor[NUM_LIGHTS];

// Posicao da camera, usada para calcular o reflexo especular.
uniform vec3 viewPos;

// Controles globais das componentes do modelo de iluminacao.
uniform float globalAmbientStrength;
uniform float globalDiffuseStrength;
uniform float globalSpecularStrength;

// Propriedades do material definidas individualmente para cada objeto.
uniform float materialDiffuse;
uniform float materialSpecular;

// Permitem escolher quais grupos de luz afetam cada objeto.
uniform bool receiveCandleLight;
uniform bool receiveExternalLight;
uniform bool candleBackfacesOnly;

// Tempo da aplicacao, usado para animar a oscilacao das velas.
uniform float time;

// Permite desenhar certos objetos apenas com sua textura.
uniform bool useLighting;

void main()
{
    // Amostra a textura nas coordenadas UV interpoladas para este fragmento.
    vec4 tex = texture(imagem, out_texture);

    // Descarta pixels quase transparentes em texturas com recortes.
    if(tex.a < 0.1)
        discard;

    // Caminho simples para objetos que nao participam da iluminacao.
    if(!useLighting)
    {
        FragColor = tex;
        return;
    }

    // A interpolacao pode alterar o comprimento da normal, por isso ela e
    // normalizada novamente antes dos produtos escalares.
    vec3 norm = normalize(Normal);

    // Iluminacao minima da cena e brilho adicional proximo das chamas.
    vec3 totalLighting = vec3(0.015 * globalAmbientStrength);
    vec3 emissiveGlow = vec3(0.0);

    //////////////////////////////////////////////////////
    // LUZES EXTERNAS (0..2)
    // Lanterna da camera e dois farois, tratados como spotlights.
    //////////////////////////////////////////////////////

    for(int i = 0; i < 3; i++)
    {
        // A lanterna (indice 0) continua disponivel para todos os objetos.
        // Os farois sao ignorados por objetos marcados como internos.
        if(!receiveExternalLight && i > 0)
            continue;

        // Vetor do fragmento ate a luz, sua distancia e sua direcao unitaria.
        vec3 lightVector = lightPos[i] - FragPos;
        float distance = length(lightVector);
        vec3 toLight = normalize(lightVector);

        // Lei do cosseno de Lambert: o produto escalar vale 1 quando a
        // superficie aponta para a luz e 0 quando nao recebe luz frontal.
        float diff = max(dot(norm, toLight), 0.0);

        // Mede o alinhamento do fragmento com o eixo central da spotlight.
        // O sinal de lightDir e invertido porque toLight aponta para a fonte.
        float theta = dot(toLight, normalize(-lightDir[i]));

        float innerCutoff;
        float outerCutoff;
        float ambientStrength;
        float linear;
        float quadratic;
        float beamStrength;

        if(i == 0)
        {
            // Lanterna: cone mais aberto e alcance mais curto.
            innerCutoff = 0.92;
            outerCutoff = 0.82;

            ambientStrength = 0.03;
            linear = 0.25;
            quadratic = 0.05;
            beamStrength = 0.40;
        }
        else
        {
            // Farois: cones estreitos, intensos e de maior alcance.
            innerCutoff = 0.992;
            outerCutoff = 0.982;

            ambientStrength = 0.0;
            linear = 0.025;
            quadratic = 0.004;
            beamStrength = 0.9;
        }

        float epsilon = innerCutoff - outerCutoff;

        // Converte theta em uma intensidade entre 0 e 1. A faixa entre os
        // dois cutoffs cria uma borda suave, em vez de um recorte brusco.
        float intensity = clamp(
            (theta - outerCutoff) / epsilon,
            0.0,
            1.0
        );

        // Atenuacao quadratica: a luz perde forca conforme a distancia cresce.
        float attenuation =
            1.0 / (1.0 + linear * distance + quadratic * distance * distance);

        // Ambiente: contribuicao constante, independente da orientacao.
        vec3 ambient =
            ambientStrength * globalAmbientStrength * lightColor[i];

        // Difusa: depende da orientacao, do cone, da distancia e do material.
        vec3 diffuse =
            diff *
            intensity *
            attenuation *
            materialDiffuse *
            globalDiffuseStrength *
            lightColor[i];

        // Reforca visualmente o centro do feixe. A potencia concentra o
        // efeito na regiao em que a intensidade da spotlight e maior.
        float beamVisibility = pow(intensity, 3.0);

        vec3 beam = beamStrength * beamVisibility * attenuation * lightColor[i];

        // Especular de Phong: compara a direcao da camera com a direcao em
        // que a luz seria refletida. O expoente 32 controla o foco do brilho.
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-toLight, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

        // O materialSpecular permite que cada objeto reflita uma quantidade
        // diferente de luz, como o carro em relacao ao chao.
        vec3 specular =
            spec *
            intensity *
            attenuation *
            materialSpecular *
            globalSpecularStrength *
            lightColor[i];

        // Acumula a contribuicao desta fonte com as fontes anteriores.
        totalLighting += ambient + diffuse + specular + beam;
    }

    //////////////////////////////////////////////////////
    // VELAS (INTERIOR)
    // Luzes pontuais: iluminam em todas as direcoes e oscilam com o tempo.
    //////////////////////////////////////////////////////

    bool candleFaceAllowed =
        !candleBackfacesOnly || !gl_FrontFacing;

    // Objetos escolhem individualmente se recebem a luz das velas. A casa
    // pode receber velas apenas nas faces internas.
    if(receiveCandleLight && candleFaceAllowed)
    {
        vec3 candleNorm = (candleBackfacesOnly && !gl_FrontFacing) ? -norm : norm;

        for(int i = 3; i < NUM_LIGHTS; i++)
        {
            // Como as velas sao pontuais, nao e necessario calcular cone.
            vec3 lightVector = lightPos[i] - FragPos;
            float distance = length(lightVector);
            vec3 toLight = normalize(lightVector);

            float diff = max(dot(candleNorm, toLight), 0.0);

            // Queda mais rapida para manter a iluminacao proxima da chama.
            float attenuation =
                1.0 / (1.0 + 0.15 * distance + 0.25 * distance * distance);

            //////////////////////////////////////////////////////
            // OSCILACAO DA CHAMA
            //////////////////////////////////////////////////////

            // O seno varia a intensidade entre 0.6 e 1.0. As coordenadas da
            // vela alteram a fase para que as quatro nao pisquem juntas.
            float flicker =
                0.80 +
                0.20 * sin(time * 8.0 + lightPos[i].x * 12.0 + lightPos[i].z * 9.0);

            // A oscilacao afeta tanto a cor percebida quanto a intensidade.
            vec3 candleColor =
                lightColor[i] * flicker;

            float intensity = flicker;

            // As velas usam as mesmas componentes ambiente, difusa e
            // especular, mas sem o calculo de spotlight.
            vec3 ambient =
                0.02  * candleColor;

            vec3 diffuse =
                diff *
                intensity *
                attenuation *
                materialDiffuse *
                globalDiffuseStrength *
                candleColor;

            vec3 viewDir = normalize(viewPos - FragPos);
            vec3 reflectDir = reflect(-toLight, candleNorm);
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

            vec3 specular =
                spec *
                intensity *
                attenuation *
                materialSpecular *
                globalSpecularStrength *
                candleColor;

            totalLighting += ambient + diffuse + specular;

            // smoothstep produz um halo que e forte junto da chama e
            // desaparece suavemente ate a distancia de 0.65 unidades.
            float flameGlow = smoothstep(0.65, 0.0, distance);
            emissiveGlow += candleColor * flameGlow * 1.8;
        }
    }

    //////////////////////////////////////////////////////
    // FINAL
    //////////////////////////////////////////////////////

    // Evita que a soma de varias fontes ultrapasse o intervalo de cor.
    totalLighting = clamp(totalLighting, 0.0, 1.0);

    // Modula a textura pela luz recebida. O halo e somado depois para se
    // comportar como emissao propria, sem depender da cor da textura.
    vec3 result = totalLighting * tex.rgb + emissiveGlow;
    result = clamp(result, 0.0, 1.0);

    // Preserva o canal alfa original da textura.
    FragColor = vec4(result, tex.a);
}
