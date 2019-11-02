#version 410 core
in vec2 Texcoord;
out vec4 outColor;

uniform sampler2D texFramebuffer;
uniform sampler2D color_texture;
uniform float pickingID;
uniform float width;
uniform float height;
void main()
{
    // texture coordinate delta
    float dxtex = 1.0 / width;  // texture width
    float dytex = 1.0 / height; // texture height

    // compare neighboring texels in the picking texture (edge detection)
    float nLeft   = texture2D(color_texture, Texcoord.st + vec2(-dxtex, 0.0)).r;
    float nRight  = texture2D(color_texture, Texcoord.st + vec2( dxtex, 0.0)).r;
    float nTop    = texture2D(color_texture, Texcoord.st + vec2( 0.0, dytex)).r;
    float nBottom = texture2D(color_texture, Texcoord.st + vec2( 0.0,-dytex)).r;
    float sum = nLeft+nRight+nTop+nBottom;

    if(sum != 4.0 * pickingID)
    {
        outColor=texture2D(color_texture,Texcoord.st);

    }
    else
        outColor=texture2D(texFramebuffer,Texcoord.st);
}