#version 410 core

// define the number of CPs in the output patch
layout (vertices = 3) out;

void main()
{
    if (gl_InvocationID == 0)
    {
        gl_TessLevelInner[0] = 50.0;
        gl_TessLevelOuter[0] = 50.0;
        gl_TessLevelOuter[1] = 50.0;
        gl_TessLevelOuter[2] = 50.0;
    }
    // Pass along the vertex position unmodified
    gl_out[gl_InvocationID].gl_Position =
    gl_in[gl_InvocationID].gl_Position;
    // Only if I am invocation 0 ...

}
