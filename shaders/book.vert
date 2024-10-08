#version 330 core

layout(location = 0) in vec3 aPos; // Vertex position
layout(location = 1) in vec3 aTexCoord; // Texture coordinate

uniform float u_flip_progress;
uniform mat4 CAMERA;

out vec3 TexCoord; // Output texture coordinate to the fragment shader

mat3 setCamera( in vec3 ro, in vec3 ta, float cr )
{
    vec3 cw = normalize(ta-ro);
    vec3 cp = vec3(sin(cr), cos(cr),0.0);
    vec3 cu = normalize( cross(cw,cp) );
    vec3 cv = normalize( cross(cu,cw) );
    return mat3( cu, cv, cw );
}

void main() {
    vec3 pagePos = aPos;
    pagePos.y = -pagePos.y;
    pagePos.x = pagePos.x*(u_flip_progress);
    mat3 hand_mat = setCamera(vec3(0., 0.0, 0.), vec3(0.5, -2.5, 5.0), -0.15);
    pagePos = hand_mat*pagePos;
    pagePos.z = -2.5-pagePos.z;
    gl_Position = CAMERA*vec4(pagePos, 1.0);
    gl_Position += vec4(1.0, -0.666,  .0, 0.);
    TexCoord = aTexCoord;
}