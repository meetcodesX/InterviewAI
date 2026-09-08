/** @type {import('next').NextConfig} */
const nextConfig = {
  // During local development, rewrite /api requests to local backend port 8000.
  // In Vercel deployment, root vercel.json service rewrites handle routing to the backend service.
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'production' 
          ? '/api/:path*' 
          : 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
