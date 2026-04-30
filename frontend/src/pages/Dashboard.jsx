import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listAssessments } from "../api/assessments";
import { getFrameworks } from "../api/frameworks";

const statusColor = { in_progress: "yellow", completed: "green" };

export default function Dashboard() {
  const [assessments, setAssessments] = useState([]);
  const [frameworks, setFrameworks] = useState([]);

  useEffect(() => {
    listAssessments().then((r) => setAssessments(r.data));
    getFrameworks().then((r) => setFrameworks(r.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">GRC Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-xl shadow p-5">
          <p className="text-sm text-gray-500">Frameworks Available</p>
          <p className="text-3xl font-bold text-indigo-600">{frameworks.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-5">
          <p className="text-sm text-gray-500">Total Assessments</p>
          <p className="text-3xl font-bold text-indigo-600">{assessments.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-5">
          <p className="text-sm text-gray-500">Completed</p>
          <p className="text-3xl font-bold text-green-600">
            {assessments.filter((a) => a.status === "completed").length}
          </p>
        </div>
      </div>

      {/* Assessments List */}
      <div className="bg-white rounded-xl shadow">
        <div className="flex justify-between items-center px-6 py-4 border-b">
          <h2 className="text-lg font-semibold">My Assessments</h2>
          <Link
            to="/assessments/new"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700"
          >
            + New Assessment
          </Link>
        </div>
        <ul className="divide-y">
          {assessments.map((a) => (
            <li key={a.id} className="px-6 py-4 flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-800">{a.name}</p>
                <p className="text-sm text-gray-500">Framework ID: {a.framework_id}</p>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`px-2 py-1 rounded-full text-xs font-medium bg-${
                    statusColor[a.status] || "gray"
                  }-100 text-${
                    statusColor[a.status] || "gray"
                  }-700`}
                >
                  {a.status}
                </span>
                <Link
                  to={`/assessments/${a.id}`}
                  className="text-indigo-600 text-sm hover:underline"
                >
                  View →
                </Link>
              </div>
            </li>
          ))}
          {assessments.length === 0 && (
            <li className="px-6 py-8 text-center text-gray-400">
              No assessments yet.{" "}
              <Link to="/assessments/new" className="text-indigo-600 underline">
                Start one
              </Link>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}
