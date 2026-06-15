#version 150 core

in vec3 position;
in vec2 texture_coord;
in vec3 normal;

out vec2 out_texture;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    vec4 worldPos = model * vec4(position, 1.0);

    FragPos = vec3(worldPos);

    Normal = mat3(transpose(inverse(model))) * normal;

    out_texture = texture_coord;

    gl_Position = projection * view * worldPos;
}