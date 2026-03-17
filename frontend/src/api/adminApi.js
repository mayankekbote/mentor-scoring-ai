import apiClient from './apiClient';

/**
 * Fetches all interview submissions for the admin dashboard.
 * @returns {Promise<Array>} List of submissions.
 */
export const getSubmissions = async () => {
  const response = await apiClient.get('/admin/submissions');
  return response.data;
};

/**
 * Fetches detailed AI evaluation results for a specific submission.
 * @param {string} submissionId - The ID of the submission.
 * @returns {Promise<Object>} Evaluation results.
 */
export const getSubmissionResults = async (submissionId) => {
  const response = await apiClient.get(`/admin/results/${submissionId}`);
  return response.data;
};

/**
 * Creates a new HR admin.
 * @param {Object} data - Admin creation data (name, email, password).
 * @returns {Promise<Object>} Success message.
 */
export const createAdmin = async (data) => {
  const response = await apiClient.post('/admin/create-admin', data);
  return response.data;
};

/**
 * Fetches all HR admins in the organization.
 * @returns {Promise<Array>} List of admins.
 */
export const getAdmins = async () => {
  const response = await apiClient.get('/admin/list-admins');
  return response.data;
};

/**
 * Generates a new unique interview code.
 * @param {Object} data - Code configuration (max_attempts, expiry_date).
 * @returns {Promise<Object>} The generated code details.
 */
export const createInterviewCode = async (data) => {
  const response = await apiClient.post('/admin/create-interview-code', data);
  return response.data;
};

/**
 * Fetches all interview codes for the organization.
 * @returns {Promise<Array>} List of interview codes.
 */
export const getInterviewCodes = async () => {
  const response = await apiClient.get('/admin/interview-codes');
  return response.data;
};

/**
 * Invites a candidate for an interview.
 * @param {string} submissionId - The ID of the submission.
 * @param {Object} data - Interview details (interview_date, interview_time).
 * @returns {Promise<Object>} Response message.
 */
export const callForInterview = async (submissionId, data) => {
  const response = await apiClient.post(`/admin/call-for-interview/${submissionId}`, data);
  return response.data;
};
