import apiClient from './apiClient';

/**
 * Validates an interview code with the backend.
 * @param {string} code - The interview code to validate.
 * @returns {Promise<Object>} The response data containing organization details if valid.
 */
export const validateInterviewCode = async (code) => {
  const response = await apiClient.post('/interview/validate-code', { code });
  return response.data;
};

/**
 * Uploads an interview video file to the backend.
 * @param {File} file - The video file to upload.
 * @param {Function} onProgress - Callback for upload progress events.
 * @returns {Promise<Object>} The response data containing the video path.
 */
export const uploadInterviewVideo = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('video_file', file);

  const response = await apiClient.post('/interview/upload-video', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentCompleted);
      }
    },
  });
  return response.data;
};

/**
 * Submits the final interview details.
 * @param {Object} data - The submission data (interview_code, topic_taught, video_path).
 * @returns {Promise<Object>} The response data.
 */
export const submitInterview = async (data) => {
  const response = await apiClient.post('/interview/submit', data);
  return response.data;
};
/**
 * Fetches the current processing status and progress of a submission.
 * @param {number|string} submissionId - The submission ID.
 * @returns {Promise<Object>} The status data (status, progress, message).
 */
export const getSubmissionStatus = async (submissionId) => {
  const response = await apiClient.get(`/interview/status/${submissionId}`);
  return response.data;
};
