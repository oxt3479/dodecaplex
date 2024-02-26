#include "window.h"
#include "shaderClass.h"
#include "shaderObjects.h"
#include "shape.h"

int main() {
    GLFWwindow* window = initializeWindow(768, 768, "SHADER");

    ShaderProgram shaderProgram("../programs/cube-vertex.glsl", \
                                "../programs/cube-fragment.glsl", true);

    VAO vertArrayObj(g_vertex_buffer_data, sizeof(g_vertex_buffer_data),\
        g_color_buffer_data, sizeof(g_color_buffer_data));
    vertArrayObj.LinkAttrib(vertArrayObj.vbo, 0, 3, GL_FLOAT, 3 * sizeof(float), (void*)0);
	vertArrayObj.LinkAttrib(vertArrayObj.cbo, 1, 3, GL_FLOAT, 3 * sizeof(float), (void*)0);

    /*VAO vertArrayObj(triforce_floats, sizeof(triforce_floats), triforce_indices, sizeof(triforce_indices));
    vertArrayObj.LinkAttrib(vertArrayObj.vbo, 0, 3, GL_FLOAT, 6 * sizeof(float), (void*)0);
	vertArrayObj.LinkAttrib(vertArrayObj.vbo, 1, 3, GL_FLOAT, 6 * sizeof(float), (void*)(3 * sizeof(float)));*/

    /*VAO vertArrayObj(vertices, sizeof(vertices), indices, sizeof(indices));
    vertArrayObj.LinkAttrib( 0, 2, GL_FLOAT, 2 * sizeof(float), (void*)0 );*/
    
    Uniforms* uniforms  = getUniforms(window);
    GLint U_RESOLUTION, U_MOUSE, U_SCROLL, U_TIME;
    
    while (!glfwWindowShouldClose(window)) {
        if (uniforms->loading) {
            shaderProgram.Load();
            shaderProgram.Activate();

            U_RESOLUTION  = glGetUniformLocation(shaderProgram.ID, "u_resolution");
            U_MOUSE       = glGetUniformLocation(shaderProgram.ID, "u_mouse");    
            U_SCROLL      = glGetUniformLocation(shaderProgram.ID, "u_scroll");
            U_TIME        = glGetUniformLocation(shaderProgram.ID, "u_time");
        }

        glClearColor(0.f, 0.f, 0.f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUniform2f(U_RESOLUTION, uniforms->windWidth, uniforms->windHeight);
        glUniform2f(U_MOUSE, uniforms->mouseX, uniforms->mouseY);        
        glUniform1f(U_SCROLL, uniforms->scroll);
        glUniform1f(U_TIME, glfwGetTime());

		//glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, 0); 
        glDrawArrays(GL_TRIANGLES, 0, 12*3);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    return 0;
}
