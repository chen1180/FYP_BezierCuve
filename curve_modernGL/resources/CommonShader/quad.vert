#version 410 core

layout (location = 0) in vec3 Position;
layout (location=1) in vec2 Uv_position;

out vec2 Texcoord;

void main()
{
    gl_Position =vec4(Position, 1.0);
    Texcoord=Uv_position;
}