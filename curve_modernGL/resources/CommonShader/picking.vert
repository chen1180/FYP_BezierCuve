#version 410

layout (location = 0) in vec3 Position;

uniform mat4 MVP;

void main()
{
    gl_Position = MVP * vec4(Position, 1.0);
}