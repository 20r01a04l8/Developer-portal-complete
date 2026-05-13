import { useState, useEffect } from 'react';
import { Box, Typography, TextField } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { useProject } from '../contexts/ProjectContext';
import { Card, Button } from '../components/common';

export const ProjectFormPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { createProject, updateProject, fetchProjectById } = useProject();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  const isEditMode = !!id;

  useEffect(() => {
    if (isEditMode) {
      fetchProjectById(id).then((data) => {
        setFormData({
          name: data.name || '',
          description: data.description || '',
        });
      });
    }
  }, [id, isEditMode, fetchProjectById]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditMode) {
        await updateProject(id, formData);
      } else {
        await createProject(formData);
      }
      navigate('/projects');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {isEditMode ? 'Edit Project' : 'Create Project'}
      </Typography>

      <Card>
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Project Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            fullWidth
          />
          <TextField
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            multiline
            rows={4}
            fullWidth
          />
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button type="submit" variant="contained">
              {isEditMode ? 'Update' : 'Create'}
            </Button>
            <Button variant="outlined" onClick={() => navigate('/projects')}>
              Cancel
            </Button>
          </Box>
        </Box>
      </Card>
    </Box>
  );
};
