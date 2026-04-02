// Configuración de la URL del backend
// En desarrollo usa localhost, en producción usa variable de entorno
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchJugadores() {
	const response = await fetch(`${API_BASE}/Jugadores/`);
	if (!response.ok) throw new Error('Error al cargar jugadores');
	return response.json();
}

export async function cargarJugador(jugadorData) {
	const response = await fetch(`${API_BASE}/Jugadores/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(jugadorData)
	});
	if (!response.ok) throw new Error('Error al registrar jugador');
	return response.json();
}

export async function subirImagenJugador(archivo) {
	const formData = new FormData();
	formData.append('archivo', archivo);

	const response = await fetch(`${API_BASE}/Jugadores/upload-imagen`, {
		method: 'POST',
		body: formData
	});

	if (!response.ok) throw new Error('Error al subir imagen');
	return response.json();
}

export async function actualizarJugador(jugadorId, jugadorData) {
	const response = await fetch(`${API_BASE}/Jugadores/${jugadorId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(jugadorData)
	});
	if (!response.ok) throw new Error('Error al actualizar jugador');
	return response.json();
}

export async function eliminarJugador(jugadorId) {
	const response = await fetch(`${API_BASE}/Jugadores/${jugadorId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		let message = 'Error al eliminar jugador';
		try {
			const data = await response.json();
			if (data?.detail) message = data.detail;
		} catch {
			// no-op
		}
		throw new Error(message);
	}
	return response.json();
}

export async function fetchEquipos() {
	const response = await fetch(`${API_BASE}/equipos/`);
	if (!response.ok) throw new Error('Error al cargar equipos');
	return response.json();
}

export async function fetchPartidos() {
	const response = await fetch(`${API_BASE}/partidos/`);
	if (!response.ok) throw new Error('Error al cargar partidos');
	return response.json();
}

export async function fetchEstadisticas() {
	const response = await fetch(`${API_BASE}/estadisticas/`);
	if (!response.ok) throw new Error('Error al cargar estadísticas');
	return response.json();
}

export async function crearPartido(partidoData) {
	const response = await fetch(`${API_BASE}/partidos/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(partidoData)
	});
	if (!response.ok) throw new Error('Error al crear partido');
	return response.json();
}

export async function actualizarPartido(partidoId, partidoData) {
	const response = await fetch(`${API_BASE}/partidos/${partidoId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(partidoData)
	});
	if (!response.ok) throw new Error('Error al actualizar partido');
	return response.json();
}

export async function eliminarPartido(partidoId) {
	const response = await fetch(`${API_BASE}/partidos/${partidoId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		let message = 'Error al eliminar partido';
		try {
			const data = await response.json();
			if (data?.detail) message = data.detail;
		} catch {
			// no-op
		}
		throw new Error(message);
	}
	return response.json();
}
