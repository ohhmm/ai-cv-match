import { useState } from 'react';
import { JobForm } from './components/JobForm';
import { ResumeUpload } from './components/ResumeUpload';
import { MatchingDashboard } from './components/MatchingDashboard';
import { Toaster } from './components/ui/toaster';
import { useToast } from './components/ui/use-toast';
import './App.css';

interface Match {
  resume: {
    skills: string[];
    experience: { years: number; description: string }[];
    education: { level: string; description: string }[];
  };
  match_details: {
    total_score: number;
    skill_match_score: number;
    preferred_skills_score: number;
    matched_required_skills: string[];
    matched_preferred_skills: string[];
  };
}

function App() {
  const { toast } = useToast();
  const [matches, setMatches] = useState<Match[]>([]);
  
  // Update matches after successful resume upload
  const updateMatches = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/matches/test-job-id/top', {
        headers: { 'Authorization': 'Bearer mock_token' }
      });
      if (!response.ok) throw new Error('Failed to fetch matches');
      const data = await response.json();
      setMatches(data);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch matches',
        variant: 'destructive',
      });
    }
  };

  const handleJobSubmit = async (requirements: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requirements }),
      });
      
      if (!response.ok) throw new Error('Failed to create job');
      
      toast({
        title: 'Success',
        description: 'Job position created successfully',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to create job position',
        variant: 'destructive',
      });
    }
  };

  const handleResumeUpload = async (files: FileList) => {
    try {
      const formData = new FormData();
      Array.from(files).forEach(file => {
        formData.append('file', file);
      });

      const response = await fetch('http://localhost:8000/api/resumes', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to upload resumes');

      toast({
        title: 'Success',
        description: 'Resumes uploaded successfully',
      });
      
      // Update matches after successful upload
      await updateMatches();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to upload resumes',
        variant: 'destructive',
      });
    }
  };

  const handleExport = () => {
    const data = JSON.stringify(matches, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'matches.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container">
      <h1 className="text-3xl font-bold mb-8">Resume Matcher</h1>
      <div className="grid">
        <JobForm onSubmit={handleJobSubmit} />
        <ResumeUpload onUpload={handleResumeUpload} />
      </div>
      <div className="mt-8">
        <MatchingDashboard matches={matches} onExport={handleExport} />
      </div>
      <Toaster />
    </div>
  );
}

export default App;
