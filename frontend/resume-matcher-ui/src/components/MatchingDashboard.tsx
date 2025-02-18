import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Download, Search, SortAsc, SortDesc } from 'lucide-react';
import { useState } from 'react';

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

interface MatchingDashboardProps {
  matches: Match[];
  onExport: () => void;
}

interface MatchingDashboardProps {
  matches: Match[];
  onExport: () => void;
}

export function MatchingDashboard({ matches, onExport }: MatchingDashboardProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState<'score' | 'experience' | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  const filteredMatches = matches.filter(match => {
    const skills = [...match.match_details.matched_required_skills, ...match.match_details.matched_preferred_skills].join(' ').toLowerCase();
    const experience = match.resume.experience.map(e => e.description).join(' ').toLowerCase();
    const education = match.resume.education.map(e => e.description).join(' ').toLowerCase();
    const searchLower = searchTerm.toLowerCase();
    
    return skills.includes(searchLower) || experience.includes(searchLower) || education.includes(searchLower);
  });

  const sortedMatches = [...filteredMatches].sort((a, b) => {
    if (!sortField) return 0;
    
    if (sortField === 'score') {
      return sortDirection === 'desc' 
        ? b.match_details.total_score - a.match_details.total_score
        : a.match_details.total_score - b.match_details.total_score;
    }
    
    if (sortField === 'experience') {
      const aYears = Math.max(...a.resume.experience.map(e => e.years), 0);
      const bYears = Math.max(...b.resume.experience.map(e => e.years), 0);
      return sortDirection === 'desc' ? bYears - aYears : aYears - bYears;
    }
    
    return 0;
  });

  const toggleSort = (field: 'score' | 'experience') => {
    if (sortField === field) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Top Matches</CardTitle>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search matches..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8"
            />
          </div>
          <Button onClick={onExport} variant="outline" size="sm">
            <Download className="mr-2 h-4 w-4" />
            Export Results
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <Button 
                  variant="ghost" 
                  onClick={() => toggleSort('score')}
                  className="flex items-center gap-2"
                >
                  Score
                  {sortField === 'score' && (
                    sortDirection === 'desc' ? <SortDesc className="h-4 w-4" /> : <SortAsc className="h-4 w-4" />
                  )}
                </Button>
              </TableHead>
              <TableHead>Skills Match</TableHead>
              <TableHead>
                <Button 
                  variant="ghost" 
                  onClick={() => toggleSort('experience')}
                  className="flex items-center gap-2"
                >
                  Experience
                  {sortField === 'experience' && (
                    sortDirection === 'desc' ? <SortDesc className="h-4 w-4" /> : <SortAsc className="h-4 w-4" />
                  )}
                </Button>
              </TableHead>
              <TableHead>Education</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedMatches.map((match, index) => (
              <TableRow key={index}>
                <TableCell>{(match.match_details.total_score * 100).toFixed(1)}%</TableCell>
                <TableCell>
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Required: {match.match_details.matched_required_skills.join(', ')}</p>
                    <p className="text-sm text-gray-500">Preferred: {match.match_details.matched_preferred_skills.join(', ')}</p>
                  </div>
                </TableCell>
                <TableCell>
                  {match.resume.experience.map((exp, i) => (
                    <p key={i} className="text-sm">{exp.years} years - {exp.description}</p>
                  ))}
                </TableCell>
                <TableCell>
                  {match.resume.education.map((edu, i) => (
                    <p key={i} className="text-sm">{edu.level} - {edu.description}</p>
                  ))}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
