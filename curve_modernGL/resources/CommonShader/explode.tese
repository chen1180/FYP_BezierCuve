#version 410 core
layout(triangles, equal_spacing, cw) in;
//The dynamic array is not support in 4.1 glsl version, constant must be passed into array.
//compute coefficient
void main()
{
    gl_Position=(gl_TessCoord.x*gl_in[0].gl_Position+gl_TessCoord.y*gl_in[1].gl_Position+gl_TessCoord.z*gl_in[2].gl_Position);
}