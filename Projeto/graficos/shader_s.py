from OpenGL.GL import *


class Shader:

    def __init__(self, vertexPath: str, fragmentPath: str):

        try:

            ##################################################
            # LER ARQUIVOS
            ##################################################

            vShaderFile = open(vertexPath)
            fShaderFile = open(fragmentPath)

            vertexCode = vShaderFile.read()
            fragmentCode = fShaderFile.read()

            vShaderFile.close()
            fShaderFile.close()

            ##################################################
            # COMPILAR VERTEX SHADER
            ##################################################

            vertex = glCreateShader(GL_VERTEX_SHADER)

            glShaderSource(vertex, vertexCode)

            glCompileShader(vertex)

            self.checkCompileErrors(vertex, "VERTEX")

            ##################################################
            # COMPILAR FRAGMENT SHADER
            ##################################################

            fragment = glCreateShader(GL_FRAGMENT_SHADER)

            glShaderSource(fragment, fragmentCode)

            glCompileShader(fragment)

            self.checkCompileErrors(fragment, "FRAGMENT")

            ##################################################
            # CRIAR PROGRAMA
            ##################################################

            self.ID = glCreateProgram()

            glAttachShader(self.ID, vertex)
            glAttachShader(self.ID, fragment)

            ##################################################
            # BIND EXPLÍCITO DOS ATRIBUTOS
            ##################################################

            # location 0 -> posição
            glBindAttribLocation(
                self.ID,
                0,
                "position"
            )

            # location 1 -> UV
            glBindAttribLocation(
                self.ID,
                1,
                "texture_coord"
            )

            # location 2 -> normal
            glBindAttribLocation(
                self.ID,
                2,
                "normal"
            )

            ##################################################
            # LINKAR PROGRAMA
            ##################################################

            glLinkProgram(self.ID)

            self.checkCompileErrors(self.ID, "PROGRAM")

            ##################################################
            # LIMPAR SHADERS
            ##################################################

            glDeleteShader(vertex)
            glDeleteShader(fragment)

        except IOError:

            print(
                "ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ"
            )

    ########################################################
    # GET PROGRAM
    ########################################################

    def getProgram(self):

        return self.ID

    ########################################################
    # USE PROGRAM
    ########################################################

    def use(self) -> None:

        glUseProgram(self.ID)

    ########################################################
    # UNIFORMS
    ########################################################

    def setBool(self, name: str, value: bool) -> None:

        glUniform1i(
            glGetUniformLocation(self.ID, name),
            int(value)
        )

    def setInt(self, name: str, value: int) -> None:

        glUniform1i(
            glGetUniformLocation(self.ID, name),
            value
        )

    def setFloat(self, name: str, value: float) -> None:

        glUniform1f(
            glGetUniformLocation(self.ID, name),
            value
        )

    ########################################################
    # CHECK ERRORS
    ########################################################

    def checkCompileErrors(
        self,
        shader: int,
        type: str
    ) -> None:

        if type != "PROGRAM":

            success = glGetShaderiv(
                shader,
                GL_COMPILE_STATUS
            )

            if not success:

                infoLog = glGetShaderInfoLog(shader)

                print(
                    "ERROR::SHADER_COMPILATION_ERROR of type: "
                    + type
                    + "\n"
                    + infoLog.decode()
                    + "\n -- --------------------------------------------------- -- "
                )

        else:

            success = glGetProgramiv(
                shader,
                GL_LINK_STATUS
            )

            if not success:

                infoLog = glGetProgramInfoLog(shader)

                print(
                    "ERROR::PROGRAM_LINKING_ERROR of type: "
                    + type
                    + "\n"
                    + infoLog.decode()
                    + "\n -- --------------------------------------------------- -- "
                )