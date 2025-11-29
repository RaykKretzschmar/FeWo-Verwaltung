/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './**/templates/**/*.html',
        '../../fewo_web/fewo/templates/**/*.html',
        '../../fewo_web/fewo/**/templates/**/*.html',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}
