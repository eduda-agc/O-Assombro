#version 150 core

in vec2 out_texture;
uniform sampler2D imagem;

out vec4 FragColor;

void main(){
    vec4 tex = texture(imagem, out_texture);
    FragColor = tex;
}