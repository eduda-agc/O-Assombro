#version 150 core

in vec2 out_texture;
out vec4 FragColor;
uniform sampler2D imagem;

void main(){
    vec4 tex = texture(imagem, out_texture);
    if(tex.a < 0.1)
        discard;  //remove pixels totalmente transparentes
    FragColor = tex;
}


