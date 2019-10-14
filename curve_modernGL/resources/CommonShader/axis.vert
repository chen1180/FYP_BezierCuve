#version 410 core
layout (location = 0) in vec3 Position_VS_in;
layout (location = 1) in vec3 Color_VS_in;
uniform mat4 MVP;

out vec3 fragmentColor;
void main()
{
    gl_Position = MVP*vec4(Position_VS_in, 1.0);
    fragmentColor=Color_VS_in;
}
