require! {
    gulp
    'gulp-less': less
    'gulp-sass': sass
    'gulp-util': gutil
    'main-bower-files': bowerfiles
    'gulp-livescript': livescript
    'gulp-browserify': browserify
}

handleError = (err) ->
    console.error err.toString!
    @emit "end"

gulp.task 'build', ['copy-js', 'copy-css', 'build-livescript', 'sass', 'browserify'] ->

gulp.task 'sass' ->
    return gulp.src './static/scss/*.scss'
           .pipe sass!
           .pipe gulp.dest './static/css'

gulp.task 'build-livescript' ->
    return gulp.src 'app/ls/**/*.ls', {base: 'app/ls'}
           .pipe livescript bare: true
           .on 'error', handleError
           .pipe gulp.dest '.tmpjs'

gulp.task 'browserify', ['build-livescript'] ->
    return gulp.src '.tmpjs/coffee.js', {base: '.tmpjs'}
    .pipe browserify {insertGlobals: true, paths: ['./node_modules', './.tmpjs']}
    .on 'error', handleError
    .pipe gulp.dest 'static/js'

gulp.task 'templates' ->
    return gulp.src './templates/*.jinja2'

gulp.task 'copy-js' ->
    return gulp.src bowerfiles ['**/*.js'], {base: './vendor'}
           .pipe gulp.dest './static/js'

gulp.task 'copy-css' ->
    return gulp.src bowerfiles ['**/*.css'], {base: './vendor'}
           .pipe gulp.dest './static/css'

