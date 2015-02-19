require! {
    gulp
    'gulp-livereload': livereload
}

gulp.task 'watch' ->
    gulp.watch 'app/ls/**/*.ls', ['build-livescript', 'browserify']
    gulp.watch 'app/scss/**/*.scss', ['sass']
