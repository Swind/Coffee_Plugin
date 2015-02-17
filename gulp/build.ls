require! {
    gulp
    'gulp-less': less
    'gulp-sass': sass
    'gulp-util': gutil
    'main-bower-files': bowerfiles
    'gulp-livescript': livescript
    'gulp-livereload': livereload
}

handleError = (err) ->
    console.error err.toString!
    @emit "end"

gulp.task 'build', ['copy-js', 'copy-css', 'build-livescript', 'sass'] ->

gulp.task 'sass' ->
    return gulp.src './static/scss/*.scss'
           .pipe sass!
           .pipe gulp.dest './static/css'
           .pipe livereload!

gulp.task 'build-livescript' ->
    return gulp.src './static/ls/*.ls'
           .pipe livescript bare: true
           .on 'error', handleError
           .pipe gulp.dest './static/js'
           .pipe livereload!

gulp.task 'templates' ->
    return gulp.src './templates/*.jinja2'
           .pipe livereload!

gulp.task 'copy-js' ->
    return gulp.src bowerfiles ['**/*.js'], {base: './vendor'}
           .pipe gulp.dest './static/js'

gulp.task 'copy-css' ->
    return gulp.src bowerfiles ['**/*.css'], {base: './vendor'}
           .pipe gulp.dest './static/css'

