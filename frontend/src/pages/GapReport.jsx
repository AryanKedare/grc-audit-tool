import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getGaps, getScore } from "../api/assessments";
import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const SEVERITY_COLORS = {
  critical: "bg-red-100 text-red-700",
  high: "bg-orange-100 text-orange-700",
  medium: "bg-yellow-100 text-yellow-700",
  low: "bg-green-100 text-green-700",
};

export default function GapReport() {
  const { id } = useParams();
  const [gaps, setGaps] = useState([]);
  const [score, setScore] = useState(null);

  useEffect(() => {
    getGaps(id).then((r) => setGaps(r.data));
    getScore(id).then((r) => setScore(r.data));
  }, [id]);

  const radarData = score
    ? {
        labels: score.domain_scores.map((d) => d.domain),
        datasets: [
          {
            label: "Compliance %",
            data: score.domain_scores.map((d) => d.score),
            backgroundColor: "rgba(99, 102, 241, 0.2)",
            borderColor: "rgba(99, 102, 241, 1)",
            pointBackgroundColor: "rgba(99, 102, 241, 1)",
          },
        ],
      }
    : null;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Gap Report</h1>
      {score && (
        <p className="text-gray-500 mb-6">
          {score.framework} — Overall Compliance:{" "}
          <span className="font-bold text-indigo-600">{score.overall_score}%</span>
          {" "}({score.answered}/{score.total_controls} controls answered)
        </p>
      )}

      {/* Radar Chart */}
      {radarData && (
        <div className="bg-white rounded-xl shadow p-6 mb-8 max-w-lg mx-auto">
          <h2 className="text-lg font-semibold mb-4 text-center">Compliance Posture by Domain</h2>
          <Radar data={radarData} options={{ scales: { r: { min: 0, max: 100 } } }} />
        </div>
      )}

      {/* Gaps Table */}
      <div className="bg-white rounded-xl shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-semibold">Identified Gaps ({gaps.length})</h2>
        </div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 uppercase text-xs">
            <tr>
              <th className="px-6 py-3 text-left">Control ID</th>
              <th className="px-6 py-3 text-left">Title</th>
              <th className="px-6 py-3 text-left">Domain</th>
              <th className="px-6 py-3 text-left">Severity</th>
              <th className="px-6 py-3 text-left">Status</th>
              <th className="px-6 py-3 text-left">Cross-Framework</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {gaps.map((gap, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="px-6 py-3 font-mono text-indigo-600">{gap.control_id}</td>
                <td className="px-6 py-3">{gap.title}</td>
                <td className="px-6 py-3 text-gray-500">{gap.domain}</td>
                <td className="px-6 py-3">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      SEVERITY_COLORS[gap.severity] || ""
                    }`}
                  >
                    {gap.severity}
                  </span>
                </td>
                <td className="px-6 py-3 capitalize">{gap.status}</td>
                <td className="px-6 py-3 text-xs text-gray-400">
                  {gap.cross_framework_refs.join(", ") || "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
