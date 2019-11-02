#version 410 core
layout(location = 0) out vec4 Frag0;
layout(location = 1) out vec4 Frag1;
in vec2 TexCoords;
uniform sampler2D texture1;

void main()
{
    Frag0 =vec4(1,0,0,1.0);
    Frag1 = texture(texture1, TexCoords);
}