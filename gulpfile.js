require('es6-promise').polyfill();

var gulp = require('gulp'),
    browserify = require('browserify'),
    concatCss = require('gulp-concat-css'),
    cleanCSS = require('gulp-clean-css'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    buffer = require('vinyl-buffer'),
    source = require('vinyl-source-stream'),
    sourcemaps = require('gulp-sourcemaps'),
    merge = require('merge-stream'),
    postcss = require('gulp-postcss'),
    pxtorem = require('postcss-pxtorem'),
    autoprefixer = require('autoprefixer'),
    shell = require('gulp-shell'),
    replace = require('gulp-replace');

var cssProcessors = [
    autoprefixer(),
    pxtorem({
        rootValue: 14,
        replace: false,
        propWhiteList: []
    })
];

gulp.task('scripts', function() {
    return browserify('./jet/static/jet/js/src/main.js')
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
    return gulp.src('./jet/static/jet/css/**/*.scss')
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
    return merge(
        gulp.src('./node_modules/jquery-ui/themes/base/images/*')
            .pipe(gulp.dest('./jet/static/jet/css/jquery-ui/images/')),
        merge(
            gulp.src([
                './node_modules/select2/dist/css/select2.css',
                './node_modules/timepicker/jquery.ui.timepicker.css'
            ]),
            gulp.src([
                './node_modules/jquery-ui/themes/base/all.css'
            ])
                .pipe(cleanCSS()) // needed to remove jQuery UI comments breaking concatCss
                .on('error', function(error) {
                    console.error(error);
                })
                .pipe(concatCss('jquery-ui.css', {
                    rebaseUrls: false
                }))
                .on('error', function(error) {
                    console.error(error);
                })
                .pipe(replace('images/', 'jquery-ui/images/'))
                .on('error', function(error) {
                    console.error(error);
                }),
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
            .pipe(concatCss('vendor.css', {
                rebaseUrls: false
            }))
            .on('error', function(error) {
                console.error(error);
            })
            .pipe(cleanCSS())
            .on('error', function(error) {
                console.error(error);
            })
            .pipe(gulp.dest('./jet/static/jet/css'))
    )
});

gulp.task('vendor-translations', function() {
    return merge(
        gulp.src(['./node_modules/jquery-ui/ui/i18n/*.js'])
            .pipe(gulp.dest('./jet/static/jet/js/i18n/jquery-ui/')),
        gulp.src(['./node_modules/timepicker/i18n/*.js'])
            .pipe(gulp.dest('./jet/static/jet/js/i18n/jquery-ui-timepicker/')),
        gulp.src(['./node_modules/select2/dist/js/i18n/*.js'])
            .pipe(gulp.dest('./jet/static/jet/js/i18n/select2/'))
    )
});

gulp.task('locales', shell.task('python manage.py compilemessages', { quiet: true }));

gulp.task('build', ['scripts', 'styles', 'vendor-styles', 'vendor-translations', 'locales']);

gulp.task('watch', function() {
    gulp.watch('./jet/static/jet/js/src/**/*.js', ['scripts']);
    gulp.watch('./jet/static/jet/css/**/*.scss', ['styles']);
    gulp.watch(['./jet/locale/**/*.po', './jet/dashboard/locale/**/*.po'], ['locales']);
});

gulp.task('default', ['build', 'watch']);
