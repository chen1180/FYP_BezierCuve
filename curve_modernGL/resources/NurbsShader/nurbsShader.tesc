#version 410 core

// define the number of CPs in the output patch
layout (vertices = 4) out;

void main()
{
    // Pass along the vertex position unmodified
        gl_out[gl_InvocationID].gl_Position =
        gl_in[gl_InvocationID].gl_Position;
       // Calculate the tessellation levels
       gl_TessLevelOuter[0] =1;
       gl_TessLevelOuter[1] = 10;
   }
