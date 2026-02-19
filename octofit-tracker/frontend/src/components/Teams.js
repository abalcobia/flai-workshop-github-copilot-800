import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Teams component: fetching from', apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Teams component: fetched data', data);
        // Support both paginated (.results) and plain array responses
        const teamList = Array.isArray(data) ? data : data.results || [];
        setTeams(teamList);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Teams component: error fetching data', err);
        setError(err.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return <div className="text-center mt-4"><div className="spinner-border" role="status" /></div>;
  if (error) return <div className="alert alert-danger mt-4">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>Teams</h2>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>Team Name</th>
            <th>Members</th>
          </tr>
        </thead>
        <tbody>
          {teams.length === 0 ? (
            <tr><td colSpan="2" className="text-center">No teams found.</td></tr>
          ) : (
            teams.map((team, index) => (
              <tr key={team._id || team.id || index}>
                <td>{team.name}</td>
                <td>
                  {Array.isArray(team.members)
                    ? team.members.join(', ')
                    : team.members}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Teams;
