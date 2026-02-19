import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts component: fetching from', apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Workouts component: fetched data', data);
        // Support both paginated (.results) and plain array responses
        const workoutList = Array.isArray(data) ? data : data.results || [];
        setWorkouts(workoutList);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Workouts component: error fetching data', err);
        setError(err.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return <div className="text-center mt-4"><div className="spinner-border" role="status" /></div>;
  if (error) return <div className="alert alert-danger mt-4">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>Workouts</h2>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {workouts.length === 0 ? (
            <tr><td colSpan="2" className="text-center">No workouts found.</td></tr>
          ) : (
            workouts.map((workout, index) => (
              <tr key={workout._id || workout.id || index}>
                <td>{workout.name}</td>
                <td>{workout.description}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Workouts;
