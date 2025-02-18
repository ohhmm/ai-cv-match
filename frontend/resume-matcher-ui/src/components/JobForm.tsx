import React from 'react';
import { Button } from './ui/button';

import { Textarea } from './ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface JobFormProps {
  onSubmit: (requirements: string) => void;
}

export function JobForm({ onSubmit }: JobFormProps) {
  const [requirements, setRequirements] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(requirements);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Add Job Position</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="requirements" className="block text-sm font-medium">
              Job Requirements
            </label>
            <Textarea
              id="requirements"
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
              placeholder="Enter job requirements..."
              className="mt-1"
              rows={5}
            />
          </div>
          <Button type="submit">Create Position</Button>
        </form>
      </CardContent>
    </Card>
  );
}
