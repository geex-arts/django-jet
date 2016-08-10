require('es6-promise').polyfill();

var gulp = require('gulp'),
    browserify = require('browserify'),
    concatCss = require('gulp-concat-css'),
    minifyCss = require('gulp-minify-css'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    buffer = require('vinyl-buffer'),
    source = require('vinyl-source-stream'),
    sourcemaps = require('gulp-sourcemaps'),
    merge = require('merge-stream'),
    postcss = require('gulp-postcss'),
    pxtorem = require('postcss-pxtorem'),
    autoprefixer = require('autoprefixer');

var cssProcessors = [
    autoprefixer(),
    pxtorem({
        rootValue: 14,
        replace: false,
        propWhiteList: []
    })
];

gulp.task('scripts', function() {
    browserify('./jet/static/jet/js/src/main.js')
        .bundle()
        .on('error', function(error) {
            console.error(error);
        })
        .pipe(source('bundle.min.js'))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest('./jet/static/jet/js/build/'));
});

gulp.task('styles', function() {
    gulp.src('./jet/static/jet/css/**/*.scss')
        .pipe(sourcemaps.init())
        .pipe(sass({
            outputStyle: 'compressed'
        }))
        .on('error', function(error) {
            console.error(error);
        })
        .pipe(postcss(cssProcessors))
        .on('error', function(error) {
            console.error(error);
        })
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./jet/static/jet/css'));
});

gulp.task('vendor-styles', function() {
    merge(
        gulp.src([
            './node_modules/select2/dist/css/select2.css',
            './node_modules/jquery-ui/themes/base/all.css',
            './node_modules/timepicker/jquery.ui.timepicker.css'
        ]),
        gulp.src([
            './node_modules/perfect-scrollbar/src/css/main.scss'
        ])
            .pipe(sass({
                outputStyle: 'compressed'
            }))
            .on('error', function(error) {
                console.error(error);
            })
    )
        .pipe(postcss(cssProcessors))
        .on('error', function(error) {
            console.error(error);
        })
        .pipe(minifyCss())
        .on('error', function(error) {
            console.error(error);
        })
        .pipe(concatCss('vendor.css'))
        .on('error', function(error) {
            console.error(error);
        })
        .pipe(gulp.dest('./jet/static/jet/css'));
});

gulp.task('vendor-translations', function() {
    gulp.src(['./node_modules/jquery-ui/ui/i18n/*.js'])
        .pipe(gulp.dest('./jet/static/jet/js/i18n/jquery-ui/'));

    gulp.src(['./node_modules/timepicker/i18n/*.js'])
        .pipe(gulp.dest('./jet/static/jet/js/i18n/jquery-ui-timepicker/'));

    gulp.src(['./node_modules/select2/dist/js/i18n/*.js'])
        .pipe(gulp.dest('./jet/static/jet/js/i18n/select2/'));
});

gulp.task('build', ['scripts', 'styles', 'vendor-styles', 'vendor-translations']);

gulp.task('watch', function() {
    gulp.watch('./jet/static/jet/js/src/**/*.js', ['scripts']);
    gulp.watch('./jet/static/jet/css/**/*.scss', ['styles']);
});

gulp.task('default', ['build', 'watch']);
