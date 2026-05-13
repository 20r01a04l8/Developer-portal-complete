import { useState, useEffect } from 'react';
import { Box, Typography, TextField } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { useTask } from '../contexts/TaskContext';
import { Card, Button } from '../components/common';

export const TaskFormPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { createTask, updateTask, fetchTaskById } = useTask();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
  });

  const isEditMode = !!id;

  useEffect(() => {
    if (isEditMode) {
      fetchTaskById(id).then((data) => {
        setFormData({
          title: data.title || '',
          description: data.description || '',
        });
      });
    }
  }, [id, isEditMode, fetchTaskById]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditMode) {
        await updateTask(id, formData);
      } else {
        await createTask(formData);
      }
      navigate('/tasks');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {isEditMode ? 'Edit Task' : 'Create Task'}
      </Typography>

      <Card>
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Task Title"
            name="title"
            value={formData.title}
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
            <Button variant="outlined" onClick={() => navigate('/tasks')}>
              Cancel
            </Button>
          </Box>
        </Box>
      </Card>
    </Box>
  );
};
