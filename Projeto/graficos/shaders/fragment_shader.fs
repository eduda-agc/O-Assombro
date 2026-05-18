#version 150 core

in vec2 out_texture;
in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

uniform sampler2D imagem;

#define NUM_LIGHTS 7

uniform vec3 lightPos[NUM_LIGHTS];
uniform vec3 lightDir[NUM_LIGHTS];
uniform vec3 lightColor[NUM_LIGHTS];

uniform vec3 candleMin;
uniform vec3 candleMax;

uniform vec3 viewPos;
uniform float globalAmbientStrength;
uniform float globalDiffuseStrength;
uniform float globalSpecularStrength;
uniform float materialDiffuse;
uniform float materialSpecular;

uniform float time;

uniform bool useLighting;

void main()
{
    vec4 tex = texture(imagem, out_texture);

    if(tex.a < 0.1)
        discard;

    if(!useLighting)
    {
        FragColor = tex;
        return;
    }

    vec3 norm = normalize(Normal);
    vec3 totalLighting = vec3(0.015 * globalAmbientStrength);
    vec3 emissiveGlow = vec3(0.0);

    bool insideCandleBox =
        FragPos.x >= candleMin.x &&
        FragPos.x <= candleMax.x &&
        FragPos.y >= candleMin.y &&
        FragPos.y <= candleMax.y &&
        FragPos.z >= candleMin.z &&
        FragPos.z <= candleMax.z;

    //////////////////////////////////////////////////////
    // LUZES EXTERNAS (0..2)
    //////////////////////////////////////////////////////

    for(int i = 0; i < 3; i++)
    {
        if(insideCandleBox && i > 0)
            continue;

        vec3 lightVector = lightPos[i] - FragPos;
        float distance = length(lightVector);
        vec3 toLight = normalize(lightVector);

        float diff = max(dot(norm, toLight), 0.0);
        float theta = dot(toLight, normalize(-lightDir[i]));

        float innerCutoff;
        float outerCutoff;
        float ambientStrength;
        float linear;
        float quadratic;
        float beamStrength;

        if(i == 0)
        {
            innerCutoff = 0.92;
            outerCutoff = 0.82;

            ambientStrength = 0.03;
            linear = 0.25;
            quadratic = 0.05;
            beamStrength = 0.40;
        }
        else
        {
            innerCutoff = 0.992;
            outerCutoff = 0.982;

            ambientStrength = 0.0;
            linear = 0.025;
            quadratic = 0.004;
            beamStrength = 0.9;
        }

        float epsilon = innerCutoff - outerCutoff;

        float intensity = clamp(
            (theta - outerCutoff) / epsilon,
            0.0,
            1.0
        );

        float attenuation =
            1.0 / (1.0 + linear * distance + quadratic * distance * distance);

        vec3 ambient =
            ambientStrength * globalAmbientStrength * lightColor[i];

        vec3 diffuse =
            diff *
            intensity *
            attenuation *
            materialDiffuse *
            globalDiffuseStrength *
            lightColor[i];

        float beamVisibility = pow(intensity, 3.0);

        vec3 beam = beamStrength * beamVisibility * attenuation * lightColor[i];

        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-toLight, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

        vec3 specular =
            spec *
            intensity *
            attenuation *
            materialSpecular *
            globalSpecularStrength *
            lightColor[i];

        totalLighting += ambient + diffuse + specular + beam;
    }

    //////////////////////////////////////////////////////
    // VELAS (INTERIOR)
    //////////////////////////////////////////////////////

    if(insideCandleBox)
    {
        for(int i = 3; i < NUM_LIGHTS; i++)
        {
            vec3 lightVector = lightPos[i] - FragPos;
            float distance = length(lightVector);
            vec3 toLight = normalize(lightVector);

            float diff = max(dot(norm, toLight), 0.0);

            float attenuation =
                1.0 / (1.0 + 0.15 * distance + 0.25 * distance * distance);

            //////////////////////////////////////////////////////
            //  FLICKER POR VELA
            //////////////////////////////////////////////////////

            float flicker =
                0.80 +
                0.20 * sin(time * 8.0 + lightPos[i].x * 12.0 + lightPos[i].z * 9.0);

            vec3 candleColor =
                lightColor[i] * flicker;

            float intensity = flicker;

            vec3 ambient =
                0.02 * globalAmbientStrength * candleColor;

            vec3 diffuse =
                diff *
                intensity *
                attenuation *
                materialDiffuse *
                globalDiffuseStrength *
                candleColor;

            vec3 viewDir = normalize(viewPos - FragPos);
            vec3 reflectDir = reflect(-toLight, norm);
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

            vec3 specular =
                spec *
                intensity *
                attenuation *
                materialSpecular *
                globalSpecularStrength *
                candleColor;

            totalLighting += ambient + diffuse + specular;

            float flameGlow = smoothstep(0.65, 0.0, distance);
            emissiveGlow += candleColor * flameGlow * 1.8;
        }
    }

    //////////////////////////////////////////////////////
    // FINAL
    //////////////////////////////////////////////////////

    totalLighting = clamp(totalLighting, 0.0, 1.0);

    vec3 result = totalLighting * tex.rgb + emissiveGlow;
    result = clamp(result, 0.0, 1.0);

    FragColor = vec4(result, tex.a);
}
