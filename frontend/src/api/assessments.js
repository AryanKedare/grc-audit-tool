import client from "./client";

export const createAssessment = (data) => client.post("/assessments", data);
export const listAssessments = () => client.get("/assessments");
export const getAssessment = (id) => client.get(`/assessments/${id}`);
export const respondToControl = (assessmentId, controlId, data) =>
  client.put(`/assessments/${assessmentId}/controls/${controlId}`, data);
export const getScore = (id) => client.get(`/assessments/${id}/score`);
export const getGaps = (id) => client.get(`/assessments/${id}/gaps`);
