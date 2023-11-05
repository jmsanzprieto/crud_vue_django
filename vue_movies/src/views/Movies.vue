<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>
        <!-- Formulario para la creación de películas -->
        <div v-if="isCreateFormVisible" class="edit-form">
          <h3 class="mb-4">Crear Película</h3>
          <form>
            <div class="row">
              <div class="col">
                <input type="text" class="form-control" v-model="newMovie.title_movie" :placeholder="'Título'">
              </div>
              <div class="col">
                <input type="text" class="form-control" v-model="newMovie.gender_movie" :placeholder="'Género'">
              </div>
              <div class="col">
                <input type="text" class="form-control" v-model="newMovie.year_movie" :placeholder="'Año'">
              </div>
              <div class="col">
                <input type="text" class="form-control" v-model="newMovie.director_movie" :placeholder="'Director'">
              </div>
              <div class="col">
                <button type="submit" class="btn btn-primary mb-2" @click="saveNewMovie">Guardar</button>
              </div>
            </div>
          </form>
        </div>
        <!-- Formulario para la creación de películas -->
        <!-- Formulario para la edición de las películas-->
        <div v-if="selectedMovieIndex !== null">
        <div class="edit-form">
          <h3 class="mb-4">Editando Película</h3>
          <form @submit.prevent="saveEditedMovie">
            <div class="row">
              <div class="col">
                <input type="text" class="form-control" v-model="movies[selectedMovieIndex].title_movie" :placeholder="'Título'">
              </div>
              <div class="col">
                <input type="text" class="form-control" v-model="movies[selectedMovieIndex].gender_movie" :placeholder="'Género'">
              </div>
              <div class="col">
                <input type="text" class="form-control" v-model="movies[selectedMovieIndex].year_movie" :placeholder="'Año'">
              </div>
              <div class="col">
                <input type="text" class="form-control" v-model="movies[selectedMovieIndex].director_movie" :placeholder="'Director'">
              </div>
              <div class="col">
                <button type="submit" class="btn btn-primary mb-2" @click="saveEditedMovie">Guardar</button>
              </div>
            </div>
          </form>
        </div>
        </div>
          <!-- Formulario para la edición de las películas-->
          <!-- Mostramos el mensaje de OK si la actualización u otra acción han ido OK -->
          <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
          </div>
          <!-- Mostramos el mensaje de OK si la actualización u otra acción han ido OK -->

          <table class="table">
            <!-- Encabezados de la tabla -->
            <thead>
              <tr>
                <th @click="toggleSortById">ID <i :class="isAscOrderById ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i></th>
                <th>Título</th>
                <th>Género</th>
                <th>Año</th>
                <th>Director</th>
                <!-- Agrega aquí más encabezados si hay más detalles -->
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <!-- Mostrar películas según la página actual -->
              <tr v-for="(movie, index) in paginatedMovies" :key="index">
                <td>{{ movie.id }}</td>
                <td>{{ movie.title_movie }}</td>
                <td>{{ movie.gender_movie }}</td>
                <td>{{ movie.year_movie }}</td>
                <td>{{ movie.director_movie }}</td>
                <!-- Muestra más detalles si es necesario -->
                <td>
                  <button class="btn btn-success" @click="editMovie(index)">Editar</button> 
                  <button class="btn btn-danger" @click="deleteMovie(index)">Borrar</button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Botones de paginación -->
          <div>
            <p><span><strong>Página</strong> {{ currentPage }}</span></p>
          </div>
          <div >
            <button class="btn btn-primary" style="margin-left: 20px;" @click="previousPage" :disabled="currentPage === 1">Anterior</button>
            <button class="btn btn-secondary" @click="nextPage" :disabled="isLastPage">Siguiente</button>
          </div>
        </div>
      </div>
      S<!-- Botón para mostrar el formulario de creación de película -->
      <button class="btn btn-primary" @click="showCreateForm">Crear Película</button>


    </div>
</template>

<script>
import { authenticateAndGetTokens } from '@/logic/auth';
import { username, password } from '@/logic/config';
import { getMovies, getMovieById, updateMovie, deleteMovieById, createMovie} from '@/logic/api_movies'; // Importa las funciones del archivo api_movies

export default {
  data() {
    return {
      movies: [],
      errorMessage: '',
      successMessage: '', 
      currentPage: 1,
      itemsPerPage: 10,
      selectedMovieIndex: null,
      isCreateFormVisible: false, 
      // Objeto para almacenar los datos de la nueva película
      newMovie: { 
        title_movie: '',
        gender_movie: '',
        year_movie: '',
        director_movie: ''
      },
      isAscOrderById: true, 
    };
  },
  computed: {
    paginatedMovies() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.movies.slice(startIndex, endIndex);
    },
    isLastPage() {
      return this.currentPage === Math.ceil(this.movies.length / this.itemsPerPage);
    }
  },
  async mounted() {
    try {
      const tokens = await authenticateAndGetTokens(username, password);
      if (tokens) {
        console.log('Autenticación exitosa:', tokens);
        this.getMoviesAndDetails(tokens.access_token);
      } else {
        this.errorMessage = 'Error en la autenticación';
      }
    } catch (error) {
      console.error('Error al conectarse a la API:', error);
      this.errorMessage = 'Error al conectar con la API';
    }
  },
  methods: {
    async getMoviesAndDetails(accessToken) {
      try {
        const movies = await getMovies(accessToken);
        if (movies) {
          console.log('Lista de películas:', movies);
          this.movies = movies;
        } else {
          this.errorMessage = 'Error al obtener la lista de películas';
        }
      } catch (error) {
        console.error('Error al obtener películas:', error);
        this.errorMessage = 'Error al obtener películas desde la API';
      }
    },
    // METODO PARA EDITAR PELICULAS
    editMovie(index) {
      this.selectedMovieIndex = index;
    },
    // METODO PARA GUARDAR LAS PELICULAS EDITADAS
    async saveEditedMovie() {
      if (this.selectedMovieIndex !== null) {
        try {
          const movieToEdit = this.movies[this.selectedMovieIndex]; // Obtener la película seleccionada para editar
          const movieId = movieToEdit.id; // Obtener el ID de la película a modificar

          const updatedMovieData = {
            // Actualiza estos campos con los datos del formulario
            title_movie: movieToEdit.title_movie, 
            gender_movie: movieToEdit.gender_movie,
            year_movie: movieToEdit.year_movie,
            director_movie: movieToEdit.director_movie,
          };

          const updatedMovie = await updateMovie(movieId, updatedMovieData);

          if (updatedMovie) {
            // Manejar la película actualizada (si es necesario)
            console.log('Película actualizada:', updatedMovie);
            // Actualizar la lista de películas
            this.movies[this.selectedMovieIndex] = updatedMovie;
            this.successMessage = '¡La película se ha actualizado correctamente!';

            // El mensaje aparece durante 2 segundos
            setTimeout(() => {
              this.successMessage = '';
            }, 2000);

          } else {
            this.errorMessage = 'Error al actualizar la película';
          }
        } catch (error) {
          console.error('Error al guardar la película editada:', error);
          this.errorMessage = 'Error al guardar la película editada';
        } finally {
          this.selectedMovieIndex = null; // Resetear la variable de índice de película seleccionada
        }
      } else {
        this.errorMessage = 'No se ha seleccionado ninguna película para editar';
      }
    },
    
    // METODO PARA BORRAR PELÍCULAS
    async deleteMovie(index) {
      const movieId = this.movies[index].id;

      if (confirm('¿Estás seguro de que quieres borrar esta película?')) {
        try {
          const deleted = await deleteMovieById(movieId);
          console.log(movieId);

          if (deleted) {
            console.log('Película eliminada con éxito');

            // Eliminar la película del array local en Vue
            //this.movies.splice(index, 1);

            this.successMessage = '¡La película se ha eliminado correctamente!';
            // El mensaje aparece durante 2 segundos
            setTimeout(() => {
              this.successMessage = '';
            }, 2000);

            // Después de eliminar, actualiza la lista de películas llamando a la función para obtener películas
            await this.getMoviesAndDetails();
          } 
        } catch (error) {
          this.errorMessage = 'Error al eliminar la película';
        }
      }
    },

    // METODO PARA MOSTRAR EL FORMULARIO DE CREACION DE PELICULAS
    showCreateForm() {
      this.isCreateFormVisible = true;
      // Limpiar los campos del nuevo formulario
      this.newMovie = {
        title_movie: '',
        gender_movie: '',
        year_movie: '',
        director_movie: ''
      };
    },

    // METODO PARA GUARDAR UNA NUEVA PELÍCULA
    async saveNewMovie() {
      if (this.newMovie.title_movie && this.newMovie.gender_movie && this.newMovie.year_movie && this.newMovie.director_movie) {
        try {
          const createdMovie = await createMovie(this.newMovie);

          if (createdMovie) {
            // Hacer algo con la película creada, por ejemplo, limpiar los campos del formulario
            this.newMovie = {
              title_movie: '',
              gender_movie: '',
              year_movie: '',
              director_movie: ''
            };

            // Actualizar la lista de películas llamando a la función para obtener películas
            await this.getMoviesAndDetails();
            
            this.successMessage = '¡La película se ha creado correctamente!';
           
            // El mensaje desaparece después de 2 segundos
            setTimeout(() => {
              this.successMessage = '';
            }, 2000);
          } else {
            this.errorMessage = 'Error al crear la película';
          }
        } catch (error) {
          console.error('Error al guardar la nueva película:', error);
          this.errorMessage = 'Error al guardar la nueva película';
        }
      } else {
        this.errorMessage = 'Por favor, completa todos los campos';
      }
    },
     // Método para alternar el orden de la lista por ID
     toggleSortById() {
      this.movies.sort((a, b) => {
        if (this.isAscOrderById) {
          return a.id - b.id;
        } else {
          return b.id - a.id;
        }
      });
      // Cambiar el estado del orden (de ascendente a descendente y viceversa)
      this.isAscOrderById = !this.isAscOrderById;
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (!this.isLastPage) {
        this.currentPage++;
      }
    }
  }
};
</script>

<style scoped>
.btn{margin: 5px;}
.edit-form {
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
