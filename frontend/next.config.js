/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable Turbopack - use Webpack instead
  experimental: {
    turbo: false,
  },
  // Disable strict mode to prevent double renders
  reactStrictMode: false,
}

module.exports = nextConfig
