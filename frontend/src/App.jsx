
import { useEffect, useState } from "react";
import "./App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState(null);
  const [dailyStats, setDailyStats] = useState([]);
  const [weeklyStats, setWeeklyStats] = useState([]);
  const [successRate, setSuccessRate] = useState(0);

  const [startDate, setStartDate] = useState("2018-06-12");
  const [endDate, setEndDate] = useState("2018-10-03");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchStats() {
      setLoading(true);
      setError(null);

      if (startDate && endDate && startDate > endDate) {
        setError("Başlangıç tarihi bitiş tarihinden büyük olamaz.");
        setLoading(false);
        return;
      }

      const params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate
      });

      try {
        const [summaryResponse, dailyResponse] = await Promise.all([
          fetch(`${API_URL}/stats/summary?${params}`, {
            signal: controller.signal
          }),
          fetch(`${API_URL}/stats/daily?${params}`, {
            signal: controller.signal
          })
        ]);

        if (!summaryResponse.ok || !dailyResponse.ok) {
          throw new Error("İstatistikler alınamadı.");
        }

        const [summaryData, dailyData] = await Promise.all([
          summaryResponse.json(),
          dailyResponse.json()
        ]);

        if (!controller.signal.aborted) {
          const totalDau = summaryData.total_dau;
          const totalSuccessful = summaryData.total_successful_players;

          const rate =
            totalDau > 0
              ? (totalSuccessful / totalDau) * 100
              : 0;

          const dailyWithRate = dailyData.map((day) => ({
            ...day,
            success_rate:
              day.dau > 0
                ? Number(((day.successful_players / day.dau) * 100).toFixed(2))
                : 0
          }));

          setSummary(summaryData);
          setDailyStats(dailyWithRate);
          setSuccessRate(Number(rate.toFixed(2)));
        }
      } catch (err) {
        if (err.name !== "AbortError") {
          setError(err.message);
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    fetchStats();



    return () => controller.abort();
  }, [startDate, endDate]);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchWeeklyStats() {
      try {
        const response = await fetch(
          `${API_URL}/stats/weekly?start_date=${startDate}&end_date=${endDate}`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          throw new Error("Haftalık veriler alınamadı.");
        }

        const data = await response.json();

        if (!controller.signal.aborted) {
          setWeeklyStats(data);
        }
      } catch (err) {
        if (err.name !== "AbortError") {
          console.error("Haftalık veri hatası:", err);
        }
      }
    }

    fetchWeeklyStats();

    return () => controller.abort();
  }, [startDate, endDate]);
    

  return (
    <main className="dashboard">
      <h1>GamePulse Dashboard</h1>
      <p>Mobile Game Analytics</p>

      {/* Tarih filtreleri */}
      <div className="date-filters">
        <label>
          Başlangıç Tarihi
          <input
            type="date"
            min="2018-06-12"
            max="2018-10-03"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>

        <label>
          Bitiş Tarihi
          <input
            type="date"
            min="2018-06-12"
            max="2018-10-03"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
      </div>

      <p className="date-info">
        Veri aralığı: 12 Haziran 2018 – 3 Ekim 2018
      </p>

      {loading && <p>Veriler güncelleniyor...</p>}

      {error && (
        <p style={{ color: "red" }}>
          Hata: {error}
        </p>
      )}

      {/* İstatistik kartları */}
      {summary && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Analiz Edilen Gün</h3>
            <h2>{summary.total_days}</h2>
          </div>

          <div className="stat-card">
            <h3>Ortalama DAU</h3>
            <h2>{summary.avg_dau}</h2>
          </div>

          <div className="stat-card">
            <h3>Günlük DAU Toplamı</h3>
            <h2>{summary.total_dau}</h2>
          </div>

          <div className="stat-card">
            <h3>Günlük Kazanan Toplamı</h3>
            <h2>{summary.total_successful_players}</h2>
          </div>

          <div className="stat-card">
            <h3>Oyuncu Başarı Oranı</h3>
            <h2>%{successRate}</h2>
          </div>
        </div>
      )}

      {/* DAU grafiği */}
      <section className="chart-card">
        <h2>Günlük Aktif Oyuncular (DAU)</h2>

        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={dailyStats}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />

            <Line
              type="monotone"
              dataKey="dau"
              stroke="#6366f1"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </section>


      <section className="chart-card">
        <h2>Günlük Kazanan ve Kaybeden Oyuncular</h2>

        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={dailyStats}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />

            <Line
              type="monotone"
              dataKey="successful_players"
              name="Kazanan Oyuncular"
              stroke="#16a34a"
              strokeWidth={2}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="failed_players"
              name="Kaybeden Oyuncular"
              stroke="#ef4444"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </section>


      <section className="chart-card">
        <h2>Günlük Oyuncu Başarı Oranı (%)</h2>

        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={dailyStats}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="date" />

            <YAxis
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />

            <Tooltip
              formatter={(value) => [`%${value}`, "Başarı Oranı"]}
            />

            <Line
              type="monotone"
              dataKey="success_rate"
              name="Başarı Oranı"
              stroke="#8b5cf6"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </section>


<section className="chart-card">
  <h2>Haftalık Ortalama Aktif Oyuncular (DAU)</h2>

  <ResponsiveContainer width="100%" height={350}>
    <LineChart data={weeklyStats}>
      <CartesianGrid strokeDasharray="3 3" />

      <XAxis dataKey="week_start" />
      <YAxis />

      <Tooltip
        formatter={(value) => [
          Number(value).toFixed(2),
          "Ortalama DAU"
        ]}
      />

      <Line
        type="monotone"
        dataKey="avg_dau"
        name="Haftalık Ortalama DAU"
        stroke="#f59e0b"
        strokeWidth={3}
        dot={{ r: 3 }}
      />
    </LineChart>
  </ResponsiveContainer>
</section>


    </main>
  );
}

export default App;
