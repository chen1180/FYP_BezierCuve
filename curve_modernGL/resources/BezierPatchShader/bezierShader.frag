#version 410 core

out vec3 FragColor;
uniform vec3 in_color;
void main()
{
    FragColor = in_color;
}
