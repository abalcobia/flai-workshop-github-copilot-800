import React, { useState, useEffect, useCallback } from 'react';

const BASE_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev`;

const FITNESS_LEVELS = ['beginner', 'intermediate', 'advanced'];

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Edit modal state
  const [editUser, setEditUser] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  const usersUrl = `${BASE_URL}/api/users/`;
  const teamsUrl = `${BASE_URL}/api/teams/`;

  const fetchUsers = useCallback(() => {
    console.log('Users component: fetching from', usersUrl);
    return fetch(usersUrl, { headers: { Accept: 'application/json' } })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        console.log('Users component: fetched data', data);
        const list = Array.isArray(data) ? data : data.results || [];
        setUsers(list);
      });
  }, [usersUrl]);

  useEffect(() => {
    // Fetch users and teams in parallel
    console.log('Users component: fetching teams from', teamsUrl);
    Promise.all([
      fetchUsers(),
      fetch(teamsUrl, { headers: { Accept: 'application/json' } })
        .then((res) => res.json())
        .then((data) => {
          console.log('Users component: fetched teams', data);
          setTeams(Array.isArray(data) ? data : data.results || []);
        }),
    ])
      .catch((err) => {
        console.error('Users component: error fetching data', err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [fetchUsers, teamsUrl]);

  const openEdit = (user) => {
    setEditUser(user);
    setEditForm({
      name: user.name || '',
      email: user.email || '',
      fitness_level: user.fitness_level || 'beginner',
      avatar: user.avatar || '',
      team: user.team != null ? String(user.team) : '',
    });
    setSaveError(null);
  };

  const closeEdit = () => {
    setEditUser(null);
    setSaveError(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveError(null);

    const payload = {
      name: editForm.name,
      email: editForm.email,
      fitness_level: editForm.fitness_level,
      avatar: editForm.avatar,
      team: editForm.team !== '' ? parseInt(editForm.team, 10) : null,
    };

    const url = `${BASE_URL}/api/users/${editUser.id}/`;
    console.log('Users component: saving to', url, payload);

    fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (!res.ok) return res.text().then((t) => { throw new Error(`HTTP ${res.status}: ${t}`); });
        return res.json();
      })
      .then((updated) => {
        console.log('Users component: saved user', updated);
        setSaving(false);
        closeEdit();
        fetchUsers();
      })
      .catch((err) => {
        console.error('Users component: save error', err);
        setSaveError(err.message);
        setSaving(false);
      });
  };

  if (loading) return <div className="text-center mt-4"><div className="spinner-border" role="status" /></div>;
  if (error) return <div className="alert alert-danger mt-4">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>Users</h2>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Team</th>
            <th>Fitness Level</th>
            <th>Avatar</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.length === 0 ? (
            <tr><td colSpan="6" className="text-center">No users found.</td></tr>
          ) : (
            users.map((user, index) => (
              <tr key={user._id || user.id || index}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.team_name || <span className="text-muted">—</span>}</td>
                <td>{user.fitness_level}</td>
                <td>{user.avatar}</td>
                <td>
                  <button
                    className="btn btn-sm btn-primary"
                    onClick={() => openEdit(user)}
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {/* Edit Modal */}
      {editUser && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <form onSubmit={handleSave}>
                <div className="modal-header">
                  <h5 className="modal-title">Edit User: {editUser.name}</h5>
                  <button type="button" className="btn-close" onClick={closeEdit} />
                </div>
                <div className="modal-body">
                  {saveError && (
                    <div className="alert alert-danger">{saveError}</div>
                  )}

                  <div className="mb-3">
                    <label className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      name="name"
                      value={editForm.name}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      name="email"
                      value={editForm.email}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Team</label>
                    <select
                      className="form-select"
                      name="team"
                      value={editForm.team}
                      onChange={handleChange}
                    >
                      <option value="">— No team —</option>
                      {teams.map((t) => (
                        <option key={t.id} value={String(t.id)}>
                          {t.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Fitness Level</label>
                    <select
                      className="form-select"
                      name="fitness_level"
                      value={editForm.fitness_level}
                      onChange={handleChange}
                    >
                      {FITNESS_LEVELS.map((lvl) => (
                        <option key={lvl} value={lvl}>
                          {lvl.charAt(0).toUpperCase() + lvl.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Avatar (emoji or initials)</label>
                    <input
                      type="text"
                      className="form-control"
                      name="avatar"
                      value={editForm.avatar}
                      onChange={handleChange}
                      maxLength={10}
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={closeEdit} disabled={saving}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={saving}>
                    {saving ? 'Saving…' : 'Save changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
