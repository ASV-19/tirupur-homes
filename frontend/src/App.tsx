import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import Home from './pages/Home';
import Properties from './pages/Properties.tsx';
import PropertyDetail from './pages/PropertyDetail.tsx';
import Login from './pages/Login';
import Admin from './pages/Admin';
import Layout from './components/Layout';
import { queryClient } from './lib/api';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Admin routes (no layout) */}
          <Route path="/login" element={<Login />} />
          <Route path="/admin" element={<Admin />} />

          {/* Public routes (with layout) */}
          <Route path="/" element={<Layout><Home /></Layout>} />
          <Route path="/properties" element={<Layout><Properties /></Layout>} />
          <Route path="/properties/:slug" element={<Layout><PropertyDetail /></Layout>} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
