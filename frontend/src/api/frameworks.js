import client from "./client";

export const getFrameworks = () => client.get("/frameworks");
export const getFramework = (id) => client.get(`/frameworks/${id}`);
export const getFrameworkControls = (id) => client.get(`/frameworks/${id}/controls`);
