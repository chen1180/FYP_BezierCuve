#version 410 core
layout(isolines) in;
uniform mat4 MVP;
out vec3 tangent;
vec3 ComputeCubicBezier(float u,vec3 p0,vec3 p1,vec3 p2,vec3 p3){
    // The patch vertices (control points)
    float u1 = (1.0 - u);
    float u2 = u * u;
    // Bernstein polynomials evaluated at u
    float b3 = u2 * u;
    float b2 = 3.0 * u2 * u1;
    float b1 = 3.0 * u * u1 * u1;
    float b0 = u1 * u1 * u1;
    // Cubic Bezier interpolation
    return (p0 * b0 + p1 * b1 + p2 * b2 + p3 *b3);
}
//tangent vector of CubicBezierCurve
vec3 ComputeCubicBezierDerivative(float u,vec3 p0,vec3 p1,vec3 p2,vec3 p3){
    vec3 a=3*(p1-p0);
    vec3 b=3*(p2-p1);
    vec3 c=3*(p3-p2);
    return a * pow(1-u,2) + 2 * b * (1-u) * u + c * pow(u,2);
}
void main()
{
    // The tessellation u coordinate
    float u = gl_TessCoord.x;
    vec3 p0 = gl_in[0].gl_Position.xyz;
    vec3 p1 = gl_in[1].gl_Position.xyz;
    vec3 p2 = gl_in[2].gl_Position.xyz;
    vec3 p3 = gl_in[3].gl_Position.xyz;
    vec3 p=ComputeCubicBezier(u,p0,p1,p2,p3);
    tangent=cross(ComputeCubicBezierDerivative(u,p0,p1,p2,p3),vec3(1,1,0));
    gl_Position = MVP*vec4(p,1.0);
}
