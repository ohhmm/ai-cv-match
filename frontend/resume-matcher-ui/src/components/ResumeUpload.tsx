import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Upload } from 'lucide-react';

interface ResumeUploadProps {
  onUpload: (files: FileList) => void;
}

export function ResumeUpload({ onUpload }: ResumeUploadProps) {
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    onUpload(e.dataTransfer.files);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      onUpload(e.target.files);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Resumes</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          className="border-2 border-dashed rounded-lg p-8 text-center"
        >
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <div className="mt-4">
            <label htmlFor="file-upload" className="cursor-pointer">
              <Button variant="outline">
                Select Files
                <input
                  id="file-upload"
                  type="file"
                  multiple
                  accept=".pdf,.doc,.docx"
                  onChange={handleChange}
                  className="hidden"
                />
              </Button>
            </label>
            <p className="mt-2 text-sm text-gray-600">
              or drag and drop files here
            </p>
            <p className="mt-1 text-xs text-gray-500">
              PDF, DOC, DOCX up to 10MB each
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
