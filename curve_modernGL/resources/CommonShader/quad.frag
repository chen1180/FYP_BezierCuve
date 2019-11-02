#version 410 core
in vec2 Texcoord;
out vec3 color;

uniform sampler2D renderedTexture;

void main(){
    color = texture( renderedTexture, Texcoord).xyz;
}