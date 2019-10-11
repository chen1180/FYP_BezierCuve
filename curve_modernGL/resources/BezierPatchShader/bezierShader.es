#version 410 core
layout(quads) in;
uniform mat4 MVP;
float Berstern(int i,float u)
{
    vec4 c=vec4(1,3,3,1);
    return c[i]*pow(u,i)*pow(1-u,3-i);
}
void main()
{
    vec4 p=vec4(0);
    // The tessellation u coordinate
    float u = gl_TessCoord.x;
    float v=gl_TessCoord.y;
    for (int j=0;j<4;++j)
    {
        for(int i=0;i<4;++i)
            {
                p+=Berstern(i,u)*Berstern(j,v)*gl_in[4*j+i].gl_Position;
            }
    }
    gl_Position = MVP*p;
}
