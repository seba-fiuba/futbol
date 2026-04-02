<script>
	import { onMount } from 'svelte';
	import {
		actualizarJugador,
		cargarJugador,
		eliminarJugador,
		fetchJugadores,
		fetchEstadisticas,
		subirImagenJugador
	} from '$lib/api';
	import { toast } from '$lib/stores/toast';

	let jugadores = [];
	let estadisticas = [];
	let loading = true;
	let error = null;
	let searchTerm = '';
	let saving = false;
	let savingEdit = false;
	let deletingJugadorId = null;
	let pendingDeleteJugadorId = null;

	let nombre = '';
	let apodo = '';
	let imagenUrl = '';
	let imagenFile = null;

	let editJugadorId = null;
	let editNombre = '';
	let editApodo = '';
	let editImagenUrl = '';
	let editImagenFile = null;

	onMount(async () => {
		try {
			[jugadores, estadisticas] = await Promise.all([
				fetchJugadores(),
				fetchEstadisticas()
			]);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	async function guardarJugador() {
		if (!nombre.trim()) {
			toast.warning('El nombre es obligatorio');
			return;
		}

		saving = true;
		error = null;
		try {
			let imagenFinal = imagenUrl.trim() || null;
			if (imagenFile) {
				const upload = await subirImagenJugador(imagenFile);
				imagenFinal = upload.url;
			}

			await cargarJugador({
				nombre: nombre.trim(),
				apodo: apodo.trim() || null,
				imagen_url: imagenFinal
			});

			[jugadores, estadisticas] = await Promise.all([
				fetchJugadores(),
				fetchEstadisticas()
			]);

			nombre = '';
			apodo = '';
			imagenUrl = '';
			imagenFile = null;
			toast.success('Jugador creado con exito');
		} catch (e) {
			error = e.message;
			toast.error(e.message || 'No se pudo crear el jugador');
		} finally {
			saving = false;
		}
	}

	function iniciarEdicion(jugador) {
		editJugadorId = jugador.id;
		editNombre = jugador.nombre || '';
		editApodo = jugador.apodo || '';
		editImagenUrl = jugador.imagen || '';
	}

	function cancelarEdicion() {
		editJugadorId = null;
		editNombre = '';
		editApodo = '';
		editImagenUrl = '';
		editImagenFile = null;
	}

	async function guardarEdicion() {
		if (!editNombre.trim() || !editJugadorId) {
			toast.warning('El nombre es obligatorio');
			return;
		}

		savingEdit = true;
		error = null;
		try {
			let imagenFinal = editImagenUrl.trim() || null;
			if (editImagenFile) {
				const upload = await subirImagenJugador(editImagenFile);
				imagenFinal = upload.url;
			}

			await actualizarJugador(editJugadorId, {
				nombre: editNombre.trim(),
				apodo: editApodo.trim() || null,
				imagen_url: imagenFinal
			});

			[jugadores, estadisticas] = await Promise.all([
				fetchJugadores(),
				fetchEstadisticas()
			]);

			cancelarEdicion();
			toast.success('Jugador actualizado con exito');
		} catch (e) {
			error = e.message;
			toast.error(e.message || 'No se pudo actualizar el jugador');
		} finally {
			savingEdit = false;
		}
	}

	function onSelectImagen(event) {
		imagenFile = event.target.files?.[0] || null;
	}

	function onSelectEditImagen(event) {
		editImagenFile = event.target.files?.[0] || null;
	}

	async function borrarJugador(jugador) {
		if (pendingDeleteJugadorId !== jugador.id) {
			pendingDeleteJugadorId = jugador.id;
			toast.warning(`Presiona Eliminar otra vez para confirmar: ${jugador.nombre}`, 2800);
			setTimeout(() => {
				if (pendingDeleteJugadorId === jugador.id) pendingDeleteJugadorId = null;
			}, 3000);
			return;
		}

		pendingDeleteJugadorId = null;

		deletingJugadorId = jugador.id;
		error = null;
		try {
			await eliminarJugador(jugador.id);
			[jugadores, estadisticas] = await Promise.all([
				fetchJugadores(),
				fetchEstadisticas()
			]);

			if (editJugadorId === jugador.id) {
				cancelarEdicion();
			}
			toast.success('Jugador eliminado con exito');
		} catch (e) {
			error = e.message;
			toast.error(e.message || 'No se pudo eliminar el jugador');
		} finally {
			deletingJugadorId = null;
		}
	}

	function getJugadorGoles(jugadorId) {
		return estadisticas
			.filter(est => est.jugador_id === jugadorId)
			.reduce((total, est) => total + est.goles, 0);
	}

	$: filteredJugadores = jugadores.filter((j) =>
		j.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
		(j.apodo && j.apodo.toLowerCase().includes(searchTerm.toLowerCase()))
	);
</script>

<svelte:head>
	<title>Jugadores - Fútbol Manager</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<h1 class="text-2xl md:text-3xl font-bold text-gray-800">👥 Jugadores</h1>
	</div>

	<!-- Alta Jugador -->
	<form on:submit|preventDefault={guardarJugador} class="bg-white rounded-lg shadow-md p-4 md:p-6 space-y-4">
		<h2 class="text-lg md:text-xl font-bold text-gray-800">Agregar jugador</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<div>
				<label for="nombre-jugador" class="block text-sm font-semibold text-gray-700 mb-2">Nombre *</label>
				<input
					id="nombre-jugador"
					type="text"
					bind:value={nombre}
					required
					placeholder="Ej: Lionel Messi"
					class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
				/>
			</div>
			<div>
				<label for="apodo-jugador" class="block text-sm font-semibold text-gray-700 mb-2">Apodo</label>
				<input
					id="apodo-jugador"
					type="text"
					bind:value={apodo}
					placeholder="Ej: La Pulga"
					class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
				/>
			</div>
			<div>
				<label for="imagen-jugador" class="block text-sm font-semibold text-gray-700 mb-2">URL imagen</label>
				<input
					id="imagen-jugador"
					type="text"
					bind:value={imagenUrl}
					placeholder="/jugadores/messi.jpg"
					class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
				/>
				<p class="text-xs text-gray-500 mt-1">Opcional: puedes pegar URL o subir archivo</p>
			</div>
			<div>
				<label for="imagen-archivo-jugador" class="block text-sm font-semibold text-gray-700 mb-2">Subir imagen</label>
				<input
					id="imagen-archivo-jugador"
					type="file"
					accept="image/png,image/jpeg,image/webp"
					on:change={onSelectImagen}
					class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white"
				/>
				<p class="text-xs text-gray-500 mt-1">JPG, PNG o WEBP (max 5MB)</p>
			</div>
		</div>
		<div class="flex justify-end">
			<button
				type="submit"
				disabled={saving}
				class="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded-lg shadow-md hover:shadow-lg transition-all disabled:bg-gray-300 disabled:cursor-not-allowed"
			>
				{saving ? 'Guardando...' : 'Guardar jugador'}
			</button>
		</div>
	</form>

	<!-- Search Bar -->
	<div class="bg-white rounded-lg shadow-md p-4">
		<input
			type="text"
			bind:value={searchTerm}
			placeholder="Buscar jugador por nombre o apodo..."
			class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
		/>
	</div>

	{#if editJugadorId}
		<form on:submit|preventDefault={guardarEdicion} class="bg-white rounded-lg shadow-md p-4 md:p-6 space-y-4 border border-blue-200">
			<h2 class="text-lg md:text-xl font-bold text-gray-800">Editar jugador</h2>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div>
					<label for="edit-nombre-jugador" class="block text-sm font-semibold text-gray-700 mb-2">Nombre *</label>
					<input
						id="edit-nombre-jugador"
						type="text"
						bind:value={editNombre}
						required
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
					/>
				</div>
				<div>
					<label for="edit-apodo-jugador" class="block text-sm font-semibold text-gray-700 mb-2">Apodo</label>
					<input
						id="edit-apodo-jugador"
						type="text"
						bind:value={editApodo}
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
					/>
				</div>
				<div>
					<label for="edit-imagen-jugador" class="block text-sm font-semibold text-gray-700 mb-2">URL imagen</label>
					<input
						id="edit-imagen-jugador"
						type="text"
						bind:value={editImagenUrl}
						placeholder="Deja vacío para quitar imagen"
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
					/>
					<p class="text-xs text-gray-500 mt-1">Opcional: URL o archivo</p>
				</div>
				<div>
					<label for="edit-imagen-archivo-jugador" class="block text-sm font-semibold text-gray-700 mb-2">Subir nueva imagen</label>
					<input
						id="edit-imagen-archivo-jugador"
						type="file"
						accept="image/png,image/jpeg,image/webp"
						on:change={onSelectEditImagen}
						class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white"
					/>
					<p class="text-xs text-gray-500 mt-1">Si eliges archivo, reemplaza la URL</p>
				</div>
			</div>
			<div class="flex flex-col sm:flex-row gap-3 sm:justify-end">
				<button
					type="button"
					on:click={cancelarEdicion}
					class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-6 py-2 rounded-lg transition-all"
				>
					Cancelar
				</button>
				<button
					type="submit"
					disabled={savingEdit}
					class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg shadow-md hover:shadow-lg transition-all disabled:bg-gray-300 disabled:cursor-not-allowed"
				>
					{savingEdit ? 'Guardando...' : 'Guardar cambios'}
				</button>
			</div>
		</form>
	{/if}

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando jugadores...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else if filteredJugadores.length === 0}
		<div class="bg-gray-50 rounded-lg p-12 text-center">
			<p class="text-gray-600 text-lg">
				{searchTerm ? 'No se encontraron jugadores' : 'No hay jugadores registrados'}
			</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
			{#each filteredJugadores as jugador}
				<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
					<div class="bg-gradient-to-br from-green-500 to-green-600 h-32 flex items-center justify-center">
						{#if jugador.imagen}
							<img src={jugador.imagen} alt={jugador.nombre} class="w-24 h-24 rounded-full object-cover border-4 border-white" />
						{:else}
							<div class="w-24 h-24 rounded-full bg-white flex items-center justify-center text-4xl border-4 border-white">
								👤
							</div>
						{/if}
					</div>
					<div class="p-4">
						<h3 class="text-xl font-bold text-gray-800 text-center">{jugador.nombre}</h3>
						{#if jugador.apodo}
							<p class="text-gray-600 text-center mt-1">"{jugador.apodo}"</p>
						{/if}
						<div class="mt-4 pt-4 border-t border-gray-200 flex items-center justify-center space-x-2">
							<span class="text-2xl">⚽</span>
							<p class="text-lg font-bold text-gray-800">{getJugadorGoles(jugador.id)} goles</p>
						</div>
						<div class="mt-3 flex justify-center gap-2">
							<button
								type="button"
								on:click={() => iniciarEdicion(jugador)}
								class="text-sm bg-blue-50 hover:bg-blue-100 text-blue-700 font-semibold px-3 py-1 rounded-lg border border-blue-200"
							>
								Editar
							</button>
							<button
								type="button"
								on:click={() => borrarJugador(jugador)}
								disabled={deletingJugadorId === jugador.id}
								class="text-sm bg-red-50 hover:bg-red-100 text-red-700 font-semibold px-3 py-1 rounded-lg border border-red-200 disabled:opacity-60"
							>
								{deletingJugadorId === jugador.id ? 'Eliminando...' : 'Eliminar'}
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>

		<div class="text-center text-gray-600">
			Mostrando {filteredJugadores.length} de {jugadores.length} jugadores
		</div>
	{/if}
</div>
