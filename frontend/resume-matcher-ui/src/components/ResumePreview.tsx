
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

interface Resume {
  skills: string[];
  experience: { years: number; description: string }[];
  education: { level: string; description: string }[];
}

interface ResumePreviewProps {
  resume: Resume;
}

export function ResumePreview({ resume }: ResumePreviewProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Resume Preview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <h3 className="font-medium mb-2">Skills</h3>
            <div className="flex flex-wrap gap-2">
              {resume.skills.map((skill, index) => (
                <Badge key={index} variant="secondary">{skill}</Badge>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="font-medium mb-2">Experience</h3>
            <div className="space-y-2">
              {resume.experience.map((exp, index) => (
                <div key={index} className="text-sm">
                  <span className="font-medium">{exp.years} years</span>
                  <p className="text-gray-600">{exp.description}</p>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="font-medium mb-2">Education</h3>
            <div className="space-y-2">
              {resume.education.map((edu, index) => (
                <div key={index} className="text-sm">
                  <span className="font-medium">{edu.level}</span>
                  <p className="text-gray-600">{edu.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
