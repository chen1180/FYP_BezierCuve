#version 410

uniform uint gDrawIndex;
uniform uint gObjectIndex;

out vec3 FragColor;

void main()
{
   FragColor = vec3(float(gObjectIndex)/255.0, float(gDrawIndex)/255.0,float(gl_PrimitiveID + 1)/255.0);
}