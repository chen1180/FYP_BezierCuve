#version 410 core

out vec4 FragColor;
uniform vec3 objectColor;
uniform vec3 lightColor;
uniform vec3 lightPos;

in vec3 normal;
in vec3 FragPos;
void main()
{
    //Ambient light
    float ambientStrength=0.7;
    vec3 ambient=ambientStrength*lightColor;
//     vec3 result = ambient* objectColor;
    //Diffuse light
    vec3 lightDir=normalize(lightPos-FragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    vec3 result = (ambient + diffuse) * objectColor;

    FragColor = vec4(result,1.0);
}
