require('es6-promise').polyfill();

var gulp = require('gulp');
var browserify = require('browserify');
var concatCss = require('gulp-concat-css');
var minifyCss = require('gulp-minify-css');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var sourcemaps = require('gulp-sourcemaps');
var merge = require('merge-stream');
var postcss = require('gulp-postcss');
var pxtorem = require('postcss-pxtorem');
var autoprefixer = require('autoprefixer');

var cssProcessors = [
    autoprefixer(),
    pxtorem({
        rootValue: 14,
        replace: false,
        propWhiteList: []
    })
];

gulp.task('js', function() {
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

gulp.task('vendor-css', function() {
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

gulp.task('vendor-i18n', function() {
    gulp.src(['./node_modules/jquery-ui/ui/i18n/*.js'])
        .pipe(gulp.dest('./jet/static/jet/js/i18n/jquery-ui/'));

    gulp.src(['./node_modules/timepicker/i18n/*.js'])
        .pipe(gulp.dest('./jet/static/jet/js/i18n/jquery-ui-timepicker/'));

    gulp.src(['./node_modules/select2/dist/js/i18n/*.js'])
        .pipe(gulp.dest('./jet/static/jet/js/i18n/select2/'));
});

gulp.task('scss', function() {
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

gulp.task('watch', function() {
    gulp.watch('./jet/static/jet/js/src/**/*.js', ['js']);
    gulp.watch('./jet/static/jet/css/**/*.scss', ['scss']);
});

gulp.task('default', ['js', 'scss', 'vendor-css', 'vendor-i18n', 'watch']);
