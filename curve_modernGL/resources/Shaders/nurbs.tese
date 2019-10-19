#version 410 core
//define the maximum vertices point that can process
#define MAX_KNOTS 32
layout(isolines) in;
//The dynamic array is not support in 4.1 glsl version, constant must be passed into array.
uniform float knots[MAX_KNOTS];
uniform float weights[MAX_KNOTS];
uniform int knots_size;
uniform int order;
uniform bool clamped;
uniform mat4 MVP;
//compute coefficient
void basicFunction(float u,int k,int p,inout float N[MAX_KNOTS]){
    //u: step (0~1)
    //k: step position in knots vector
    //p: order of the curve
    if (clamped==true){
        if (u==1.0){
            N[gl_PatchVerticesIn-1]=1.0;
            return;
        } else if(u==0.0){
            N[0]=1.0;
            return;
        }

    }
    N[k] = 1.0;
    for(int d=1;d<p+1;d++){
        N[k - d] = (knots[k + 1] - u) / (knots[k + 1] - knots[(k - d) + 1]) * N[(k - d) + 1];
        for(int i=k-d+1;i<k;i++){
            N[i] = (u - knots[i]) /(knots[i + d] - knots[i])* N[i] + (knots[i + d + 1] - u) / (knots[i + d + 1] - knots[i + 1]) * N[i + 1];
        }
        N[k] = (u - knots[k]) / (knots[k + d] - knots[k]) * N[k];
    }
}
vec3 deBoor(float u,int k,int p){
    vec3 pArray[MAX_KNOTS];
    for (int j=0;j<p+1;j++){
        pArray[j]=gl_in[k-p+j].gl_Position.xyz;
    }
    for (int r = 1;r <= p;++r)
    {
        for (int i = k,j=p;i >= k - p+r;--i,--j)
        {
            float alpha = u - knots[i];
            float dev = (knots[i+p+1-r]-knots[i]);
            alpha = (dev !=0.0)? alpha / dev : 0;
            pArray[j] = (1.0 - alpha)*pArray[j - 1] + alpha * pArray[j];
        }
    }
    return  pArray[p];
}
void main()
{
    // The tessellation u coordinate
    float u = gl_TessCoord.x;
    //order
    int p=order;
    //number of vertices
    int n=gl_PatchVerticesIn;
    //Discard all the points between [knots[p],knots[m-p-1]]
    if (clamped==false){
        if((u<knots[p])||(u>knots[knots_size-p-1]))
        return;
    }
    //Initialize N array
    float N[MAX_KNOTS];
    for (int i=0;i<knots_size;i++){
        N[i]=0;
    }
    //find the knotspan of u in knots
    int k=0;
    for (int i=0;i<knots_size-1;i++){
        if ((u >= knots[i])&&(u < knots[i+1]))
        {
            k=i;
            break;
        }
    }
    vec3 lastP;
    //calculate value of N
    basicFunction(u, k, p, N);
    for (int i=0;i<gl_PatchVerticesIn;i++){
        lastP+=gl_in[i].gl_Position.xyz*N[i]*weights[i];
    }
    float W=0;
    for(int i=0;i<knots_size;i++)
    {
        W+=weights[i]*N[i];
    }
    lastP/=W;
    gl_Position = MVP*vec4(lastP,1.0);
}