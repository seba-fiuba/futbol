<script>
	import { onMount } from 'svelte';
	import {
		actualizarEquipoTorneo,
		actualizarJugadorTorneo,
		actualizarPartidoTorneo,
		actualizarTorneo,
		crearEquipoTorneo,
		crearJugadorTorneo,
		crearPartidoTorneo,
		crearTorneo,
		eliminarEquipoTorneo,
		eliminarJugadorTorneo,
		eliminarPartidoTorneo,
		eliminarTorneo,
		fetchEquiposTorneo,
		fetchJugadores,
		fetchJugadoresTorneo,
		fetchPartidosTorneo,
		fetchTorneos
	} from '$lib/api';
	import { toast } from '$lib/stores/toast';

	let loading = true;
	let error = null;
	let warning = null;

	let torneos = [];
	let equiposTorneo = [];
	let partidosTorneo = [];
	let jugadoresTorneo = [];
	let jugadoresBase = [];

	let selectedTorneoId = '';

	let nuevoTorneoNombre = '';
	let nuevoTorneoEstado = 'abierto';

	let editTorneoId = null;
	let editTorneoNombre = '';
	let editTorneoEstado = 'abierto';
	let pendingDeleteTorneoId = null;

	let nuevoEquipoNombre = '';
	let editEquipoId = null;
	let editEquipoNombre = '';
	let pendingDeleteEquipoId = null;

	let nuevoPartidoLocalId = '';
	let nuevoPartidoVisitanteId = '';
	let nuevaFase = 'liga';
	let editPartidoId = null;
	let editPartidoGolesLocal = 0;
	let editPartidoGolesVisitante = 0;
	let editPartidoFase = 'liga';
	let editPartidoJugado = false;
	let pendingDeletePartidoId = null;

	let nuevoJugadorEquipoId = '';
	let nuevoJugadorUsuarioId = '';
	let editJugadorTorneoId = null;
	let editJugadorEquipoId = '';
	let pendingDeleteJugadorTorneoId = null;

	onMount(async () => {
		await cargarTodo();
	});

	async function cargarTodo() {
		loading = true;
		error = null;
		warning = null;
		try {
			const [torneosRes, equiposRes, partidosRes, jugadoresTorneoRes, jugadoresRes] = await Promise.allSettled([
				fetchTorneos(),
				fetchEquiposTorneo(),
				fetchPartidosTorneo(),
				fetchJugadoresTorneo(),
				fetchJugadores()
			]);

			if (torneosRes.status === 'rejected') {
				throw torneosRes.reason;
			}

			const torneosData = torneosRes.value;
			const equiposData = equiposRes.status === 'fulfilled' ? equiposRes.value : [];
			const partidosData = partidosRes.status === 'fulfilled' ? partidosRes.value : [];
			const jugadoresTorneoData =
				jugadoresTorneoRes.status === 'fulfilled' ? jugadoresTorneoRes.value : [];
			const jugadoresData = jugadoresRes.status === 'fulfilled' ? jugadoresRes.value : [];

			const fallosParciales = [];
			if (equiposRes.status === 'rejected') fallosParciales.push('equipos de torneo');
			if (partidosRes.status === 'rejected') fallosParciales.push('partidos de torneo');
			if (jugadoresTorneoRes.status === 'rejected') fallosParciales.push('planteles del torneo');
			if (jugadoresRes.status === 'rejected') fallosParciales.push('jugadores base');

			if (fallosParciales.length > 0) {
				warning = `Se cargó parcialmente. Falló: ${fallosParciales.join(', ')}.`;
			}

			torneos = torneosData.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion));
			equiposTorneo = equiposData;
			partidosTorneo = partidosData;
			jugadoresTorneo = jugadoresTorneoData;
			jugadoresBase = jugadoresData;

			if (selectedTorneoId && torneos.some((t) => String(t.id) === String(selectedTorneoId))) {
				selectedTorneoId = String(selectedTorneoId);
			} else {
				selectedTorneoId = torneos[0] ? String(torneos[0].id) : '';
			}
		} catch (e) {
			error = e?.message || 'No se pudo cargar torneos';
		} finally {
			loading = false;
		}
	}

	function formatFecha(fecha) {
		if (!fecha) return '-';
		return new Date(fecha).toLocaleDateString('es-AR', {
			day: '2-digit',
			month: '2-digit',
			year: 'numeric'
		});
	}

	function getJugadorNombre(jugadorId) {
		const jugador = jugadoresBase.find((j) => j.id === jugadorId);
		if (!jugador) return `Jugador #${jugadorId}`;
		return jugador.apodo ? `${jugador.nombre} "${jugador.apodo}"` : jugador.nombre;
	}

	function getEquipoNombre(equipoId) {
		const equipo = equiposTorneo.find((e) => e.id === equipoId);
		return equipo ? equipo.nombre : `Equipo #${equipoId}`;
	}

	async function handleCrearTorneo() {
		if (!nuevoTorneoNombre.trim()) {
			toast.warning('El nombre del torneo es obligatorio');
			return;
		}

		try {
			const torneoCreado = await crearTorneo({
				nombre: nuevoTorneoNombre.trim(),
				estado: nuevoTorneoEstado
			});
			nuevoTorneoNombre = '';
			nuevoTorneoEstado = 'abierto';
			await cargarTodo();
			selectedTorneoId = String(torneoCreado.id);
			toast.success('Torneo creado con exito');
		} catch (e) {
			toast.error(e.message || 'No se pudo crear el torneo');
		}
	}

	function iniciarEdicionTorneo(torneo) {
		editTorneoId = torneo.id;
		editTorneoNombre = torneo.nombre;
		editTorneoEstado = torneo.estado;
	}

	function cancelarEdicionTorneo() {
		editTorneoId = null;
		editTorneoNombre = '';
		editTorneoEstado = 'abierto';
	}

	async function guardarEdicionTorneo() {
		if (!editTorneoId || !editTorneoNombre.trim()) {
			toast.warning('El nombre del torneo es obligatorio');
			return;
		}

		try {
			await actualizarTorneo(editTorneoId, {
				nombre: editTorneoNombre.trim(),
				estado: editTorneoEstado
			});
			await cargarTodo();
			cancelarEdicionTorneo();
			toast.success('Torneo actualizado con exito');
		} catch (e) {
			toast.error(e.message || 'No se pudo actualizar el torneo');
		}
	}

	async function borrarTorneo(torneo) {
		if (pendingDeleteTorneoId !== torneo.id) {
			pendingDeleteTorneoId = torneo.id;
			toast.warning(`Presiona Eliminar otra vez para confirmar: ${torneo.nombre}`, 2800);
			setTimeout(() => {
				if (pendingDeleteTorneoId === torneo.id) pendingDeleteTorneoId = null;
			}, 3000);
			return;
		}

		pendingDeleteTorneoId = null;
		try {
			await eliminarTorneo(torneo.id);
			if (String(torneo.id) === String(selectedTorneoId)) {
				selectedTorneoId = '';
			}
			await cargarTodo();
			toast.success('Torneo eliminado con exito');
		} catch (e) {
			toast.error(e.message || 'No se pudo eliminar el torneo');
		}
	}

	async function handleCrearEquipo() {
		if (!selectedTorneoId) {
			toast.warning('Selecciona un torneo primero');
			return;
		}
		if (!nuevoEquipoNombre.trim()) {
			toast.warning('El nombre del equipo es obligatorio');
			return;
		}

		try {
			await crearEquipoTorneo({
				torneo_id: Number(selectedTorneoId),
				nombre: nuevoEquipoNombre.trim()
			});
			nuevoEquipoNombre = '';
			await cargarTodo();
			toast.success('Equipo agregado al torneo');
		} catch (e) {
			toast.error(e.message || 'No se pudo crear el equipo');
		}
	}

	function iniciarEdicionEquipo(equipo) {
		editEquipoId = equipo.id;
		editEquipoNombre = equipo.nombre;
	}

	function cancelarEdicionEquipo() {
		editEquipoId = null;
		editEquipoNombre = '';
	}

	async function guardarEdicionEquipo() {
		if (!editEquipoId || !editEquipoNombre.trim()) {
			toast.warning('El nombre del equipo es obligatorio');
			return;
		}
		try {
			await actualizarEquipoTorneo(editEquipoId, { nombre: editEquipoNombre.trim() });
			await cargarTodo();
			cancelarEdicionEquipo();
			toast.success('Equipo actualizado');
		} catch (e) {
			toast.error(e.message || 'No se pudo actualizar el equipo');
		}
	}

	async function borrarEquipo(equipo) {
		if (pendingDeleteEquipoId !== equipo.id) {
			pendingDeleteEquipoId = equipo.id;
			toast.warning(`Presiona Eliminar otra vez para confirmar: ${equipo.nombre}`, 2800);
			setTimeout(() => {
				if (pendingDeleteEquipoId === equipo.id) pendingDeleteEquipoId = null;
			}, 3000);
			return;
		}

		pendingDeleteEquipoId = null;
		try {
			await eliminarEquipoTorneo(equipo.id);
			await cargarTodo();
			toast.success('Equipo eliminado');
		} catch (e) {
			toast.error(e.message || 'No se pudo eliminar el equipo');
		}
	}

	async function handleCrearPartido() {
		if (!selectedTorneoId) {
			toast.warning('Selecciona un torneo primero');
			return;
		}
		if (!nuevoPartidoLocalId || !nuevoPartidoVisitanteId) {
			toast.warning('Selecciona equipo local y visitante');
			return;
		}
		if (nuevoPartidoLocalId === nuevoPartidoVisitanteId) {
			toast.warning('Local y visitante deben ser diferentes');
			return;
		}

		try {
			await crearPartidoTorneo({
				torneo_id: Number(selectedTorneoId),
				local_id: Number(nuevoPartidoLocalId),
				visitante_id: Number(nuevoPartidoVisitanteId),
				fase: nuevaFase.trim() || 'liga'
			});
			nuevoPartidoLocalId = '';
			nuevoPartidoVisitanteId = '';
			nuevaFase = 'liga';
			await cargarTodo();
			toast.success('Partido de torneo creado');
		} catch (e) {
			toast.error(e.message || 'No se pudo crear el partido');
		}
	}

	function iniciarEdicionPartido(partido) {
		editPartidoId = partido.id;
		editPartidoGolesLocal = Number(partido.goles_local ?? 0);
		editPartidoGolesVisitante = Number(partido.goles_visitante ?? 0);
		editPartidoFase = partido.fase || 'liga';
		editPartidoJugado = Boolean(partido.jugado);
	}

	function cancelarEdicionPartido() {
		editPartidoId = null;
		editPartidoGolesLocal = 0;
		editPartidoGolesVisitante = 0;
		editPartidoFase = 'liga';
		editPartidoJugado = false;
	}

	async function guardarEdicionPartido() {
		if (!editPartidoId) return;
		if (Number(editPartidoGolesLocal) < 0 || Number(editPartidoGolesVisitante) < 0) {
			toast.warning('Los goles no pueden ser negativos');
			return;
		}

		try {
			await actualizarPartidoTorneo(editPartidoId, {
				goles_local: Number(editPartidoGolesLocal),
				goles_visitante: Number(editPartidoGolesVisitante),
				fase: editPartidoFase,
				jugado: editPartidoJugado
			});
			await cargarTodo();
			cancelarEdicionPartido();
			toast.success('Partido actualizado');
		} catch (e) {
			toast.error(e.message || 'No se pudo actualizar el partido');
		}
	}

	async function borrarPartido(partido) {
		if (pendingDeletePartidoId !== partido.id) {
			pendingDeletePartidoId = partido.id;
			toast.warning('Presiona Eliminar otra vez para confirmar', 2800);
			setTimeout(() => {
				if (pendingDeletePartidoId === partido.id) pendingDeletePartidoId = null;
			}, 3000);
			return;
		}

		pendingDeletePartidoId = null;
		try {
			await eliminarPartidoTorneo(partido.id);
			await cargarTodo();
			toast.success('Partido eliminado');
		} catch (e) {
			toast.error(e.message || 'No se pudo eliminar el partido');
		}
	}

	async function handleAgregarJugadorATorneo() {
		if (!nuevoJugadorEquipoId || !nuevoJugadorUsuarioId) {
			toast.warning('Selecciona un equipo y un jugador');
			return;
		}

		const existeEnTorneo = jugadoresDelTorneo.some(
			(j) => String(j.usuario_id) === String(nuevoJugadorUsuarioId)
		);
		if (existeEnTorneo) {
			toast.warning('Ese jugador ya esta en este torneo');
			return;
		}

		try {
			await crearJugadorTorneo({
				equipo_torneo_id: Number(nuevoJugadorEquipoId),
				usuario_id: Number(nuevoJugadorUsuarioId)
			});
			nuevoJugadorUsuarioId = '';
			await cargarTodo();
			toast.success('Jugador agregado al torneo');
		} catch (e) {
			toast.error(e.message || 'No se pudo agregar el jugador');
		}
	}

	function iniciarEdicionJugadorTorneo(jugadorTorneo) {
		editJugadorTorneoId = jugadorTorneo.id;
		editJugadorEquipoId = String(jugadorTorneo.equipo_torneo_id);
	}

	function cancelarEdicionJugadorTorneo() {
		editJugadorTorneoId = null;
		editJugadorEquipoId = '';
	}

	async function guardarEdicionJugadorTorneo() {
		if (!editJugadorTorneoId || !editJugadorEquipoId) {
			toast.warning('Selecciona un equipo');
			return;
		}
		try {
			await actualizarJugadorTorneo(editJugadorTorneoId, {
				equipo_torneo_id: Number(editJugadorEquipoId)
			});
			await cargarTodo();
			cancelarEdicionJugadorTorneo();
			toast.success('Jugador movido de equipo');
		} catch (e) {
			toast.error(e.message || 'No se pudo mover el jugador');
		}
	}

	async function borrarJugadorTorneo(jugadorTorneo) {
		if (pendingDeleteJugadorTorneoId !== jugadorTorneo.id) {
			pendingDeleteJugadorTorneoId = jugadorTorneo.id;
			toast.warning('Presiona Eliminar otra vez para confirmar', 2800);
			setTimeout(() => {
				if (pendingDeleteJugadorTorneoId === jugadorTorneo.id) pendingDeleteJugadorTorneoId = null;
			}, 3000);
			return;
		}
		pendingDeleteJugadorTorneoId = null;

		try {
			await eliminarJugadorTorneo(jugadorTorneo.id);
			await cargarTodo();
			toast.success('Jugador eliminado del torneo');
		} catch (e) {
			toast.error(e.message || 'No se pudo eliminar el jugador del torneo');
		}
	}

	$: torneoSeleccionado = torneos.find((t) => String(t.id) === String(selectedTorneoId));
	$: equiposDelTorneo = equiposTorneo.filter((e) => String(e.torneo_id) === String(selectedTorneoId));
	$: partidosDelTorneo = partidosTorneo.filter((p) => String(p.torneo_id) === String(selectedTorneoId));
	$: idsEquiposDelTorneo = new Set(equiposDelTorneo.map((e) => e.id));
	$: jugadoresDelTorneo = jugadoresTorneo.filter((j) => idsEquiposDelTorneo.has(j.equipo_torneo_id));
</script>

<svelte:head>
	<title>Torneos - Fútbol Manager</title>
</svelte:head>

<div class="space-y-6">
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
		<h1 class="text-2xl md:text-3xl font-bold text-gray-800">🏟️ Torneos</h1>
		<p class="text-sm text-gray-600">Gestiona torneos, equipos, planteles y partidos</p>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando seccion de torneos...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
			<button
				type="button"
				on:click={cargarTodo}
				class="mt-3 inline-block bg-red-600 hover:bg-red-700 text-white text-sm font-semibold px-4 py-2 rounded-lg"
			>
				Reintentar
			</button>
		</div>
	{:else}
		{#if warning}
			<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
				<p class="font-semibold">Aviso:</p>
				<p>{warning}</p>
			</div>
		{/if}
		<div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
			<section class="xl:col-span-1 space-y-4">
				<div class="bg-white rounded-lg shadow-md p-4 space-y-3">
					<h2 class="text-lg font-bold text-gray-800">Crear torneo</h2>
					<input
						type="text"
						bind:value={nuevoTorneoNombre}
						placeholder="Nombre del torneo"
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
					/>
					<select
						bind:value={nuevoTorneoEstado}
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
					>
						<option value="abierto">Abierto</option>
						<option value="en curso">En curso</option>
						<option value="finalizado">Finalizado</option>
					</select>
					<button
						type="button"
						on:click={handleCrearTorneo}
						class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded-lg"
					>
						Crear torneo
					</button>
				</div>

				<div class="bg-white rounded-lg shadow-md p-4 space-y-3">
					<h2 class="text-lg font-bold text-gray-800">Torneos ({torneos.length})</h2>
					{#if torneos.length === 0}
						<p class="text-gray-600 text-sm">Aun no hay torneos registrados.</p>
					{:else}
						<div class="space-y-3 max-h-[70vh] overflow-y-auto pr-1">
							{#each torneos as torneo}
								<div class="border rounded-lg p-3 {String(selectedTorneoId) === String(torneo.id) ? 'border-green-500 bg-green-50' : 'border-gray-200'}">
									{#if editTorneoId === torneo.id}
										<div class="space-y-2">
											<input
												type="text"
												bind:value={editTorneoNombre}
												class="w-full px-3 py-2 border border-gray-300 rounded-lg"
											/>
											<select bind:value={editTorneoEstado} class="w-full px-3 py-2 border border-gray-300 rounded-lg">
												<option value="abierto">Abierto</option>
												<option value="en curso">En curso</option>
												<option value="finalizado">Finalizado</option>
											</select>
											<div class="flex gap-2">
												<button type="button" on:click={guardarEdicionTorneo} class="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm">Guardar</button>
												<button type="button" on:click={cancelarEdicionTorneo} class="flex-1 bg-gray-200 px-3 py-2 rounded-lg text-sm">Cancelar</button>
											</div>
										</div>
									{:else}
										<div class="flex items-start justify-between gap-2">
											<button
												type="button"
												on:click={() => (selectedTorneoId = String(torneo.id))}
												class="text-left flex-1"
											>
												<h3 class="font-semibold text-gray-800">{torneo.nombre}</h3>
												<p class="text-xs text-gray-600">{torneo.estado} • {formatFecha(torneo.fecha_creacion)}</p>
											</button>
											<div class="flex items-center gap-2">
												<button type="button" on:click={() => iniciarEdicionTorneo(torneo)} class="text-sm text-blue-700">Editar</button>
												<button type="button" on:click={() => borrarTorneo(torneo)} class="text-sm text-red-700">Eliminar</button>
											</div>
										</div>
									{/if}
								</div>
							{/each}
						</div>
					{/if}
				</div>
			</section>

			<section class="xl:col-span-2 space-y-4">
				{#if !torneoSeleccionado}
					<div class="bg-gray-50 rounded-lg p-8 text-center text-gray-600">
						Selecciona o crea un torneo para empezar.
					</div>
				{:else}
					<div class="bg-white rounded-lg shadow-md p-4 md:p-5">
						<h2 class="text-xl font-bold text-gray-800">{torneoSeleccionado.nombre}</h2>
						<p class="text-sm text-gray-600 mt-1">Estado: {torneoSeleccionado.estado} • Creado: {formatFecha(torneoSeleccionado.fecha_creacion)}</p>
					</div>

					<div class="bg-white rounded-lg shadow-md p-4 md:p-5 space-y-4">
						<div class="flex items-center justify-between">
							<h3 class="text-lg font-bold text-gray-800">🛡️ Equipos del torneo</h3>
							<span class="text-sm text-gray-600">{equiposDelTorneo.length}</span>
						</div>
						<div class="flex flex-col sm:flex-row gap-3">
							<input
								type="text"
								bind:value={nuevoEquipoNombre}
								placeholder="Nombre del equipo"
								class="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
							/>
							<button type="button" on:click={handleCrearEquipo} class="bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded-lg">Agregar equipo</button>
						</div>

						{#if equiposDelTorneo.length === 0}
							<p class="text-sm text-gray-600">No hay equipos cargados en este torneo.</p>
						{:else}
							<div class="grid grid-cols-1 md:grid-cols-2 gap-3">
								{#each equiposDelTorneo as equipo}
									<div class="border rounded-lg p-3">
										{#if editEquipoId === equipo.id}
											<div class="space-y-2">
												<input type="text" bind:value={editEquipoNombre} class="w-full px-3 py-2 border border-gray-300 rounded-lg" />
												<div class="flex gap-2">
													<button type="button" on:click={guardarEdicionEquipo} class="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm">Guardar</button>
													<button type="button" on:click={cancelarEdicionEquipo} class="flex-1 bg-gray-200 px-3 py-2 rounded-lg text-sm">Cancelar</button>
												</div>
											</div>
										{:else}
											<div class="flex items-center justify-between gap-2">
												<div>
													<p class="font-semibold text-gray-800">{equipo.nombre}</p>
													<p class="text-xs text-gray-600">ID #{equipo.id}</p>
												</div>
												<div class="flex gap-2">
													<button type="button" on:click={() => iniciarEdicionEquipo(equipo)} class="text-sm text-blue-700">Editar</button>
													<button type="button" on:click={() => borrarEquipo(equipo)} class="text-sm text-red-700">Eliminar</button>
												</div>
											</div>
										{/if}
									</div>
								{/each}
							</div>
						{/if}
					</div>

					<div class="bg-white rounded-lg shadow-md p-4 md:p-5 space-y-4">
						<div class="flex items-center justify-between">
							<h3 class="text-lg font-bold text-gray-800">👤 Planteles</h3>
							<span class="text-sm text-gray-600">{jugadoresDelTorneo.length}</span>
						</div>
						<div class="grid grid-cols-1 md:grid-cols-3 gap-3">
							<select bind:value={nuevoJugadorEquipoId} class="px-4 py-2 border border-gray-300 rounded-lg">
								<option value="">Equipo</option>
								{#each equiposDelTorneo as equipo}
									<option value={String(equipo.id)}>{equipo.nombre}</option>
								{/each}
							</select>
							<select bind:value={nuevoJugadorUsuarioId} class="px-4 py-2 border border-gray-300 rounded-lg">
								<option value="">Jugador</option>
								{#each jugadoresBase as jugador}
									<option value={String(jugador.id)}>{getJugadorNombre(jugador.id)}</option>
								{/each}
							</select>
							<button type="button" on:click={handleAgregarJugadorATorneo} class="bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded-lg">Agregar jugador</button>
						</div>

						{#if jugadoresDelTorneo.length === 0}
							<p class="text-sm text-gray-600">No hay jugadores asignados en este torneo.</p>
						{:else}
							<div class="space-y-2 max-h-72 overflow-y-auto pr-1">
								{#each jugadoresDelTorneo as jt}
									<div class="border rounded-lg p-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
										<div>
											<p class="font-semibold text-gray-800">{getJugadorNombre(jt.usuario_id)}</p>
											<p class="text-sm text-gray-600">Equipo: {getEquipoNombre(jt.equipo_torneo_id)}</p>
										</div>
										{#if editJugadorTorneoId === jt.id}
											<div class="flex flex-col sm:flex-row gap-2 sm:items-center">
												<select bind:value={editJugadorEquipoId} class="px-3 py-2 border border-gray-300 rounded-lg text-sm">
													<option value="">Mover a...</option>
													{#each equiposDelTorneo as equipo}
														<option value={String(equipo.id)}>{equipo.nombre}</option>
													{/each}
												</select>
												<button type="button" on:click={guardarEdicionJugadorTorneo} class="bg-blue-600 text-white px-3 py-2 rounded-lg text-sm">Guardar</button>
												<button type="button" on:click={cancelarEdicionJugadorTorneo} class="bg-gray-200 px-3 py-2 rounded-lg text-sm">Cancelar</button>
											</div>
										{:else}
											<div class="flex gap-3 text-sm">
												<button type="button" on:click={() => iniciarEdicionJugadorTorneo(jt)} class="text-blue-700">Mover</button>
												<button type="button" on:click={() => borrarJugadorTorneo(jt)} class="text-red-700">Eliminar</button>
											</div>
										{/if}
									</div>
								{/each}
							</div>
						{/if}
					</div>

					<div class="bg-white rounded-lg shadow-md p-4 md:p-5 space-y-4">
						<div class="flex items-center justify-between">
							<h3 class="text-lg font-bold text-gray-800">⚽ Partidos del torneo</h3>
							<span class="text-sm text-gray-600">{partidosDelTorneo.length}</span>
						</div>
						<div class="grid grid-cols-1 md:grid-cols-4 gap-3">
							<select bind:value={nuevoPartidoLocalId} class="px-4 py-2 border border-gray-300 rounded-lg">
								<option value="">Local</option>
								{#each equiposDelTorneo as equipo}
									<option value={String(equipo.id)}>{equipo.nombre}</option>
								{/each}
							</select>
							<select bind:value={nuevoPartidoVisitanteId} class="px-4 py-2 border border-gray-300 rounded-lg">
								<option value="">Visitante</option>
								{#each equiposDelTorneo as equipo}
									<option value={String(equipo.id)}>{equipo.nombre}</option>
								{/each}
							</select>
							<input type="text" bind:value={nuevaFase} placeholder="Fase (liga, semis...)" class="px-4 py-2 border border-gray-300 rounded-lg" />
							<button type="button" on:click={handleCrearPartido} class="bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded-lg">Crear partido</button>
						</div>

						{#if partidosDelTorneo.length === 0}
							<p class="text-sm text-gray-600">No hay partidos en este torneo.</p>
						{:else}
							<div class="space-y-3">
								{#each partidosDelTorneo as partido}
									<div class="border rounded-lg p-3">
										<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
											<div>
												<p class="font-semibold text-gray-800">{getEquipoNombre(partido.local_id)} vs {getEquipoNombre(partido.visitante_id)}</p>
												<p class="text-sm text-gray-600">Fase: {partido.fase} • {partido.jugado ? 'Jugado' : 'Pendiente'}</p>
											</div>
											<div class="text-lg font-bold text-green-700">{partido.goles_local ?? 0} - {partido.goles_visitante ?? 0}</div>
										</div>

										{#if editPartidoId === partido.id}
											<div class="mt-3 grid grid-cols-1 md:grid-cols-5 gap-2">
												<input type="number" min="0" bind:value={editPartidoGolesLocal} class="px-3 py-2 border border-gray-300 rounded-lg" />
												<input type="number" min="0" bind:value={editPartidoGolesVisitante} class="px-3 py-2 border border-gray-300 rounded-lg" />
												<input type="text" bind:value={editPartidoFase} class="px-3 py-2 border border-gray-300 rounded-lg" />
												<label class="flex items-center gap-2 text-sm px-3 py-2 border border-gray-300 rounded-lg">
													<input type="checkbox" bind:checked={editPartidoJugado} />
													Jugado
												</label>
												<div class="flex gap-2">
													<button type="button" on:click={guardarEdicionPartido} class="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm">Guardar</button>
													<button type="button" on:click={cancelarEdicionPartido} class="flex-1 bg-gray-200 px-3 py-2 rounded-lg text-sm">Cancelar</button>
												</div>
											</div>
										{:else}
											<div class="mt-3 flex gap-3 text-sm">
												<button type="button" on:click={() => iniciarEdicionPartido(partido)} class="text-blue-700">Editar</button>
												<button type="button" on:click={() => borrarPartido(partido)} class="text-red-700">Eliminar</button>
											</div>
										{/if}
									</div>
								{/each}
							</div>
						{/if}
					</div>
				{/if}
			</section>
		</div>
	{/if}
</div>
