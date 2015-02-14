require! {
    gulp
    'gulp-livereload': livereload
}

gulp.task 'watch' ->
    livereload.options.host = "192.168.1.169"
    livereload.listen!
    gulp.watch 'static/ls/*.ls', ['build-livescript']
    gulp.watch 'static/scss/*.scss', ['sass']
    gulp.watch 'templates/*.jinja2', ['templates']
