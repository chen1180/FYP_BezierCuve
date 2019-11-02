#version 410 core
layout( triangles ) in;
layout( points, max_vertices=3 ) out;
uniform int uLevel;
uniform float uGravity;
uniform float uTime;
uniform float uVelScale;
uniform mat4 MVP;
vec3 V0, V01, V02;
vec3 CG;
void ProduceVertex( float s, float t )
{
    vec3 norm=normalize(cross(V01,V02));
    vec3 v = V0 + s*V01 + t*V02;
    vec3 vel = uVelScale * ( v - CG );
//    v = CG + vel*uTime + 0.5*vec3(0.,uGravity,0.)*uTime*uTime;
    v = CG + vel*uTime+ 0.5*vec3(0.,uGravity,0.)*uTime*uTime;
    gl_Position = MVP * vec4( v, 1. );
    EmitVertex( );
    EndPrimitive();
}
void main()
{
    V01 = ( gl_PositionIn[1] - gl_PositionIn[0] ).xyz;
    V02 = ( gl_PositionIn[2] - gl_PositionIn[0] ).xyz;
    V0 = gl_PositionIn[0].xyz;
    CG = ( gl_PositionIn[0].xyz + gl_PositionIn[1].xyz + gl_PositionIn[2].xyz ) / 3.;
    int numLayers = 1 << uLevel;
    float dt = 1. / float( numLayers );
    float t = 1.;
    for( int it = 0; it <= numLayers; it++ )
    {
        float smax = 1. - t;
        int nums = it + 1;
        float ds = smax / float( nums - 1 );
        float s = 0.;
        for( int is = 0; is < nums; is++ )
        {
            ProduceVertex( s, t );
            s += ds;
        }
        t -= dt;
    }
}
